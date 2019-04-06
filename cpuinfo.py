#!/usr/bin/env python

import json
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)

def get_cpu_info(file_path):
    cpuinfo = {}
    with open(file_path) as fd:
        for line in fd:
            try:
                key, value = extract_values(line)
                if key.lower() == "processor":
                    processor = value
                    cpuinfo[processor] = {} 
                # note: this breaks if processor is not the first key
                else:
                    cpuinfo[processor][key] = value
            except ValueError:
                # empty line => next processor
                pass
    # TOTALS
    real  = len({cpuinfo[k]['physical_id'] for k in cpuinfo.keys()})
    cores = len({cpuinfo[k]['cpu_cores']   for k in cpuinfo.keys()}) 
    # add entries
    cpuinfo['real']  = real       # physical CPUs
    cpuinfo['cores'] = cores      # cores per CPU
    cpuinfo['total'] = real*cores # logical CPUs
    return cpuinfo

def extract_values(line):
    key, value = line.split(':')
    key, value = key.strip(), value.strip()
    key = key.replace(' ', '_')
    # values as lists
    if key.lower() in ("flags", "bugs"):
        value = value.split()
    return key, value

class HTTPHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        data = json.dumps(get_cpu_info('/proc/cpuinfo'))
        self.wfile.write(bytes(data, "utf8"))
        
def run(server_class=HTTPServer, handler_class=HTTPHandler, port=8080):
    httpd = server_class(('', port), handler_class)
    print("Server started!")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
# END
