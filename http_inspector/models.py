import json
from urllib.parse import urlparse

from . import utils


def json_body_enhancer(content):
    try:
        return json.dumps(json.loads(content), indent=2)
    except json.JSONDecodeError:
        return content


BODY_ENHANCERS = {"application/json": json_body_enhancer}


class Request:
    def __init__(self, method, client_address, path, headers, stream):
        parsed = urlparse(path)

        self.path = path
        self.client_address, self.client_port = client_address
        self.clean_path = parsed.path
        self.params = {}
        params = parsed.query

        if params:
            params = params.split("&")
            for param in params:
                key, value = param.split("=")
                self.params.setdefault(key, [])
                self.params[key].append(value)

        self.method = method.upper()
        self.headers = headers

        self.content_length = int(self.headers.get("Content-Length") or 0)
        self.content_type = self.headers.get("Content-Type")
        self.encoding = utils.get_encoding_from_headers(self.content_type)

        self.__body = stream.read(self.content_length)

    @property
    def _body(self):
        encoding = self.encoding or "utf-8"
        return self.__body.decode(encoding)

    @property
    def body(self):
        body = self._body
        if self.content_type and self.content_type.lower() in BODY_ENHANCERS:
            enhancer = BODY_ENHANCERS[self.content_type.lower()]
            return enhancer(body)
        return body

    @property
    def length_in_human(self):
        return f"{self.content_length} bytes"
