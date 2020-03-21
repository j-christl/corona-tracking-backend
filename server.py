import logging
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl
from socketserver import ThreadingMixIn
import json

from cfg.config import config
from backend.database import Database
from rest.response import ErrorResponse
from rest.request import RegisterUserRequest, UploadTrackRequest, UpdateUserStatusRequest
from rest.core import RequestProcessor


logger = logging.getLogger("corona")
ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


request_processor = None


class RequestFactory:
    @staticmethod
    def get(method, path, params, body):
        assert isinstance(method, str)
        assert isinstance(path, str)
        assert isinstance(params, dict)
        assert isinstance(body, dict)

        split_path = path.split("/")
        split_path.pop(0)
        try:
            if method == "POST":
                if split_path[0] == "register":
                    return RegisterUserRequest(params=params)
                elif split_path[0] == "track":
                    return UploadTrackRequest(params=params, body=body)
                else:
                    raise ValueError("Invalid path")
            elif method == "PATCH":
                if split_path[0] == "status":
                    return UpdateUserStatusRequest(params=params)
                else:
                    raise ValueError("Invalid path")
            else:
                raise ValueError("Invalid path")
        except Exception as ex:
            logger.error("EXCEPTION PARSING REQUEST: {} {}".format(type(ex), ex))
            return ErrorResponse(str(ex))


class RequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        return

    def do_GET(self):
        self._do_request("GET")

    def do_POST(self):
        self._do_request("POST")

    def do_PATCH(self):
        self._do_request("PATCH")

    def _do_request(self, method):
        assert isinstance(method, str)

        logger.info(method + ": {}".format(self.path))
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = dict(parse_qsl(parsed_path.query))
        logger.debug("PARAMS: {}".format(params))

        # get request body
        content_type = self.headers.get("Content-Type")
        if content_type != "application/json":
            self.send_response(415)
            self.end_headers()
            self.wfile.write("Content-Type must be application/json".encode("utf-8"))
            self.wfile.write(b"\n")
            return
        content_len = int(self.headers.get("Content-Length"))
        body = json.load(self.rfile.read(content_len))

        result = RequestFactory.get(method=method, path=path, params=params, body=body)
        if isinstance(result, ErrorResponse):
            response = result
        else:
            logger.debug('CREATED REQUEST: {} {}'.format(type(result), result))
            response = request_processor.process_request(request=result)

        self.send_response(response.response_code)
        self.end_headers()
        self.wfile.write(response.to_string().encode("utf-8"))
        self.wfile.write(b"\n")


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def main():

    if not Database.initialize():
        Database.terminate()
        return

    global request_processor
    request_processor = RequestProcessor()

    params = config("httpserver")
    hostname = params["host"]
    port = int(params["port"])

    logger.info("starting http server...")
    server = ThreadingHTTPServer((hostname, port), RequestHandler)
    logger.info("listening on {}:{}...".format(hostname, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("HTTP SERVER STOPPED")
    Database.terminate()


if __name__ == '__main__':
    if sys.version_info[0] < 3:
        logger.error('Must be using Python 3')
    else:
        main()
