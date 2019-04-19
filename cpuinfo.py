#!/usr/bin/env python

##########################################
# Code Challenge - New Relic - Barcelona #
# Francesc Vendrell | Apr 2019           #
##########################################

import sys

from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)

from lib.util import get_cpu_info_alt

class HTTPHandler(BaseHTTPRequestHandler):
    """Simple GET-only HTTP Server"""

    cpuinfo = get_cpu_info_alt()
    default_port = 8080

    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        try:
            self._set_headers(200)
            self.wfile.write(HTTPHandler.cpuinfo)
        except Exception as ex:
            self._set_headers(500)
            self.wfile.write(to_bytes({'error': str(ex)}))
            
def run():
    try:
        port = int(sys.argv[1])
    except:
        port = HTTPHandler.default_port

    httpd = HTTPServer(('', port), HTTPHandler)
    print(f'Server started at port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

# END
