import asyncio
import logging
import os
from functools import partial

import aiofiles
from aiohttp import web

from arg_parser import get_parser

BUF_SIZE = 100 * 1024

logger = logging.getLogger(__file__)


async def archive(request, storage_dir):

    response = web.StreamResponse()
    archive_name = request.match_info.get("archive_hash", "")
    error = False
    files_directory_path = os.path.abspath(os.path.join(storage_dir, archive_name))
    if not os.path.exists(f"..{files_directory_path}"):
        async with aiofiles.open("templates/page_404.html", mode="r") as index_file:
            index_contents = await index_file.read()
        raise web.HTTPNotFound(text=index_contents, content_type="text/html")

    response.headers["Content-Type"] = "text/html"
    response.headers["Content-Disposition"] = f'attachment; filename="{archive_name}.zip"'

    process = await asyncio.subprocess.create_subprocess_exec(
        "zip",
        "-r",
        "-",
        ".",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=f"..{os.path.join(storage_dir)}/{archive_name}",
    )
    await response.prepare(request)
    logger.info("Download begins")
    try:
        while True:
            stdout = await process.stdout.read(BUF_SIZE)
            if process.stdout.at_eof():
                break

            await response.write(stdout)
            logger.debug("Sending archive chunk ...")
    except BaseException:
        logger.error("Download was interrupted!")
        error = True
        process.kill()
        await process.communicate()
        raise
    finally:
        if not error:
            logger.info("Download is complete")
            return response


async def handle_index_page(request):
    async with aiofiles.open("templates/index.html", mode="r") as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    logging_level = (
        int(os.environ.get("LOGGING_LEVEL"))
        if os.environ.get("LOGGING_LEVEL")
        else args.logs
    )

    logging.basicConfig(
        format="%(levelname)-8s [%(asctime)s] %(message)s",
        level=logging_level,
    )

    storage_dir = os.environ.get("STORAGE_DIR") or args.storage_dir
    get_archive = partial(archive, storage_dir=storage_dir)

    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_index_page),
            web.get("/archive/{archive_hash}/", get_archive),
        ]
    )
    web.run_app(app)
