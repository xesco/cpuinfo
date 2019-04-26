#!/usr/bin/env python

import sys

from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)

from lib.util import get_cpu_info, to_bytes

DEFAULT_PORT = 8080


class MyHTTPServer(HTTPServer):
    """HTTP server with an extra parameter to serve only 'data' """
    def __init__(self, server_address, RequestHandlerClass, data):
        super().__init__(server_address, RequestHandlerClass)
        self.data = data
    

class HTTPHandler(BaseHTTPRequestHandler):
    """Simple GET-only HTTP Server"""

    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        try:
            self._set_headers(200)
            # from the handler class we can access the server class
            self.wfile.write(self.server.data)
        except Exception as ex:
            self._set_headers(500)
            self.wfile.write(to_bytes({'error': str(ex)}))
            
def run():
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        port = DEFAULT_PORT

    try:
        data = get_cpu_info()    
    except FileNotFoundError:
        print("Error: /proc/cpuinfo not found :(")
    except UnboundLocalError:
        sys.stderr.write('Error: /proc/cpuinfo format not supported :(\n')
    # All good
    else:
        httpd = MyHTTPServer(('', port), HTTPHandler, data)
        print(f'Server started at port {port}')
        httpd.serve_forever()

if __name__ == '__main__':
    run()

# END
