import json
import logging
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qsl

from backend.database import Database
from cfg.config import config
from rest.core import RequestProcessor
from rest.request import RegisterUserRequest, UploadTrackRequest, UpdateUserStatusRequest, GetUserStatusRequest
from rest.response import ErrorResponse

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
                if split_path[0] == "userstatus":
                    return UpdateUserStatusRequest(params=params)
                else:
                    raise ValueError("Invalid path")
            elif method == "GET":
                if split_path[0] == "userstatus":
                    return GetUserStatusRequest(params=params)
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

        remote_ip = self.client_address[0]
        logger.info("Incoming request from {}".format(remote_ip))
        logger.info(method + ": {}".format(self.path))
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = dict(parse_qsl(parsed_path.query))
        logger.debug("PARAMS: {}".format(params))

        # get request body
        body = None
        if method == "POST" or method == "PATCH":
            content_type = self.headers.get("Content-Type")
            if content_type != "application/json":
                self.send_response(415)
                self.end_headers()
                self.wfile.write("Content-Type must be application/json".encode("utf-8"))
                self.wfile.write(b"\n")
                return
            content_len = self.headers["Content-Length"]
            logger.debug("Content-Length: " + str(content_len))
            if content_len is not None:
                content_len = int(content_len)
                if content_len > 0:
                    content = self.rfile.read(content_len).decode("utf-8")
                    logger.debug("BODY: {}".format(content))
                    body = json.loads(content)

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
