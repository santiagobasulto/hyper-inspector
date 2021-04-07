import pathlib
import argparse

from .logger.rich_logger import RichLogger
from .logger.file_logger import FileLogger

from .server import DebugServer


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def main():
    parser = argparse.ArgumentParser(
        prog="http_inspector", description="Inspect and debug HTTP requests"
    )

    parser.add_argument(
        "-r",
        "--response",
        type=int,
        default=200,
        help="default response for every incoming request",
    )
    parser.add_argument(
        "-f",
        "--enable-file-logging",
        type=str2bool,
        nargs="?",
        const=True,
        default=True,
        help="Enable file logging",
    )
    parser.add_argument(
        "-d",
        "--logging-directory",
        default=".",
        type=pathlib.Path,
        help="Directory to store logs",
    )
    parser.add_argument(
        "--log-body",
        type=str2bool,
        nargs="?",
        default=True,
        const=True,
        help="Should it log the whole body to the console.",
    )

    parser.add_argument("--ip", default="", help="IP Addr to serve")
    parser.add_argument(
        "--port", type=int, default=5555, help="Server Port to listen to"
    )

    args = parser.parse_args()

    loggers = [RichLogger(args), FileLogger(args)]

    httpd = DebugServer(
        address=args.ip, port=args.port, response=args.response, loggers=loggers
    )

    try:
        print(f"Serving on addr {args.ip} and port {args.port}...")
        print("(To stop the server press Control+C)")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Closing connection...")
    httpd.server_close()


if __name__ == "__main__":
    main()
