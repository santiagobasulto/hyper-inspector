from functools import partialmethod
from http.server import BaseHTTPRequestHandler

from .models import Request


class DebugRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(self.server.debug_response)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_X(self, method):
        request = Request(
            method, self.client_address, self.path, self.headers, self.rfile
        )
        self._set_response()

        for logger in self.server.loggers:
            logger.log(request)
        self.wfile.write(f"{request.method} - {request.path} received".encode("utf-8"))

    do_GET = partialmethod(do_X, "GET")
    do_POST = partialmethod(do_X, "POST")
    do_PUT = partialmethod(do_X, "PUT")
    do_PATCH = partialmethod(do_X, "PATCH")
    do_DELETE = partialmethod(do_X, "DELETE")

    do_HEAD = partialmethod(do_X, "HEAD")
    do_OPTIONS = partialmethod(do_X, "OPTIONS")
