from http.server import HTTPServer


from .handler import DebugRequestHandler


class DebugServer(HTTPServer):
    DEFAULT_HANDLER = DebugRequestHandler

    def __init__(self, address="", port=5555, handler=None, response=200, loggers=None):
        super().__init__((address, port), handler or self.DEFAULT_HANDLER)
        self.debug_response = response
        self.loggers = loggers or []
