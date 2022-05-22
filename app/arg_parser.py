import argparse


def get_parser():
    parser = argparse.ArgumentParser(description="Microservice for downloading files")
    parser.add_argument(
        "--storage_dir",
        type=str,
        default="/test_photos",
        help="Storage directory (default: /test_photos)",
    )
    parser.add_argument(
        "--logs",
        type=int,
        default=10,
        help="type=int, default=100, Possible values: DISABLE=100, CRITICAL=50, ERROR=40, "
             "WARNING=30, INFO=20, DEBUG=10, NONSET=0",
    )

    return parser
