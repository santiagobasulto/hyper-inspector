import json
from datetime import datetime

from rich import print, box

from rich.table import Table
from rich.panel import Panel
from rich.console import Console, RenderGroup
from rich.text import Text
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.padding import Padding

import pygments.lexers

from . import BaseLogger


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


class RichLogger(BaseLogger):
    def log(self, request):
        title = Text()
        title.append(request.method, style="bold red")
        title.append(" ")
        path = request.path
        if len(path) > 50:
            path = request.path[:50] + "..."
        title.append(path, style="blue")

        headers_table = Table(
            title="[bold]HTTP Headers\n", title_justify="center", show_edge=False
        )
        headers_table.add_column(
            "Header", justify="left", style="magenta", no_wrap=True
        )
        headers_table.add_column(
            "Value", justify="right", style="cyan",
        )

        for header, value in request.headers.items():
            if header.lower() in {"content-type", "content-length"}:
                continue
            headers_table.add_row(header, value)

        local_time, utc_time = datetime.now(), datetime.utcnow()
        group = [
            Text.assemble(
                ("Local Time: ", "bold"),
                local_time.strftime(TIME_FORMAT),
                " - ",
                ("UTC Time: ", "bold"),
                utc_time.strftime(TIME_FORMAT),
                justify="center",
            ),
            Text.assemble(
                ("Content Type: ", "bold"),
                (str(request.content_type), "italic magenta"),
                " - ",
                (request.length_in_human, "cyan"),
            ),
            Text.assemble(
                ("Client's IP/Port: ", "bold"),
                f"{request.client_address}:{request.client_port}",
            ),
        ]

        # Query Params
        if request.params:
            params_table = Table(
                title="[bold]Query Params[/bold] (accepts repeated)\n",
                title_justify="center",
                show_edge=False,
            )
            params_table.add_column(
                "Param", justify="left", style="magenta", no_wrap=True
            )
            params_table.add_column(
                "Value", justify="right", style="cyan",
            )

            for param, values in request.params.items():
                params_table.add_row(param, ",".join(values))
            group.append(Padding(params_table, (1,)))

        # Headers
        group.append(Padding(headers_table, (1,)))

        # Request Body
        if "log_body" in self.args and self.args.log_body:
            if request.body:
                group += [
                    Padding("[bold]Request Body:[/bold]", (1,)),
                    Syntax(
                        request.body,
                        pygments.lexers.get_lexer_for_mimetype(
                            request.content_type
                        ).name,
                        word_wrap=True,
                    ),
                ]
            else:
                group.append(
                    Padding("[bold]Request Body: [/bold][italic]Empty.[/italic]", (1,)),
                )

        # Display it all
        print(Panel(RenderGroup(*group), title=title, box=box.ROUNDED, highlight=True,))
