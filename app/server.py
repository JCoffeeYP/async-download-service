import asyncio
import logging
import os

import aiofiles
from aiohttp import web

from arg_parser import get_parser


parser = get_parser()
args = parser.parse_args()

BUF_SIZE = 100 * 1024
# LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL")) or args.logs
# STORAGE_DIR = os.environ.get("STORAGE_DIR") or args.storage_dir
LOGGING_LEVEL = args.logs
STORAGE_DIR = args.storage_dir

logging.basicConfig(
    format="%(levelname)-8s [%(asctime)s] %(message)s",
    level=LOGGING_LEVEL,
)


async def archive(request):
    response = web.StreamResponse()
    archive_name = request.match_info.get("archive_hash", "")
    error = False
    files_directory_path = os.path.abspath(os.path.join(STORAGE_DIR, archive_name))
    if not os.path.exists(f"..{files_directory_path}"):
        async with aiofiles.open("templates/page_404.html", mode="r") as index_file:
            index_contents = await index_file.read()
        raise web.HTTPNotFound(text=index_contents, content_type="text/html")

    response.headers["Content-Type"] = "text/html"
    response.headers["Content-Disposition"] = f'attachment; filename="{archive_name}.zip"'

    cmd = f"zip -jr - {archive_name}"
    process = await asyncio.subprocess.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=f"..{os.path.join(STORAGE_DIR)}"
    )

    await response.prepare(request)
    logging.info("Download begins")
    try:
        while True:
            stdout = await process.stdout.read(BUF_SIZE)
            if process.stdout.at_eof():
                break

            await response.write(stdout)
            logging.debug("Sending archive chunk ...")
    except BaseException:
        logging.error("Download was interrupted!")
        error = True
        process_pid = process.pid
        await process.communicate()
        await asyncio.create_subprocess_exec(
            "sh",
            "./subprocess_kill.sh",
            f"{process_pid}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        raise
    finally:
        if not error:
            logging.info("Download is complete")
            return response


async def handle_index_page(request):
    async with aiofiles.open("templates/index.html", mode="r") as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(
        [
            web.get("/", handle_index_page),
            web.get("/archive/{archive_hash}/", archive),
        ]
    )
    web.run_app(app)
