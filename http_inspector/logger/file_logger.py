import json
import mimetypes
import rich

from datetime import datetime

from . import BaseLogger


class FileLogger(BaseLogger):
    def log(self, request):
        if not self.args.enable_file_logging:
            return
        if not self.args.logging_directory.exists():
            rich.print(
                f"[red bold]Error: Can't write file logs because directory [italic]{str(self.args.logging_directory)}[/italic] doesn't exist"
            )
            return
        path_name = ".".join(request.clean_path.split("/")[1:]) or "(root)"
        base_file_name = (
            f"{request.method.upper()}.{path_name}.{int(datetime.utcnow().timestamp())}"
        )

        request_file_name = base_file_name + ".request.json"

        with (self.args.logging_directory / request_file_name).open("w") as fp:
            fp.write(
                json.dumps(
                    {
                        "method": request.method,
                        "clean_path": request.clean_path,
                        "path": request.path,
                        "query_params": request.params,
                        "headers": {**request.headers},
                        "content_length": request.content_length,
                        "content_type": request.content_type,
                        "encoding": request.encoding,
                    },
                    indent=2,
                )
            )
        if request.body:
            ext = mimetypes.guess_extension(request.content_type) or ".txt"
            body_file_name = base_file_name + ".body" + ext
            with (self.args.logging_directory / body_file_name).open("w") as fp:
                fp.write(request.body)
