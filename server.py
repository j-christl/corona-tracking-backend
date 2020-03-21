import logging
import sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl

from config import config
from database import Database

logger = logging.getLogger("corona")
ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class RequestHandler(BaseHTTPRequestHandler):
    """ handle http GET requests. """

    def log_message(self, format, *args):
        """ do nothing """
        return

    def do_POST(self):
        logger.info("POST: {}".format(self.path))
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = dict(parse_qsl(parsed_path.query))
        logger.debug("PARAMS: {}".format(params))

        # TODO update database

        self.send_response(400)
        self.end_headers()
        self.wfile.write("Insert data here")
        self.wfile.write(b"\n")


def main():

    if not Database.initialize():
        Database.terminate()
        return

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
