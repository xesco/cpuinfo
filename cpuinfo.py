#!/usr/bin/env python

##########################################
# Code Challenge - New Relic - Barcelona #
# Francesc Vendrell | Apr 2019           #
##########################################

import json
import sys

from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler,
)

DEFAULT_PORT = 8080

def get_totals(cpuinfo):
    # We assume same CPU architecture for multi CPU systems
    real     = len({cpuinfo[k]['physical_id'] for k in cpuinfo.keys()})
    cores    = int(cpuinfo['0']['cpu_cores'])
    total    = real*cores

    # Hyperthreading support (added for completeness)
    siblings = int(cpuinfo['0']['siblings'])
    if cores != siblings:
        cpuinfo['siblings'] = siblings
        total *= siblings
    return real, cores, total

def get_cpu_info(file_path='/proc/cpuinfo'):
    """Get System's CPU/s specifications as a dict"""
    cpuinfo = {}
    with open(file_path) as fd:
        for line in fd:
            try:
                key, value = extract_values(line)
                if key == 'processor':
                    processor = value
                    cpuinfo[processor] = {} 
                else:
                   # note: this breaks if 'processor' is not the first key
                    cpuinfo[processor][key] = value
            except ValueError:
                # empty line => next processor
                pass
            except UnboundLocalError:
                # this should not happen
                sys.stderr.write('Error: /proc/cpuinfo format not supported :(\n')
                sys.exit(1)
    cpuinfo['real'], cpuinfo['cores'], cpuinfo['total'] = get_totals(cpuinfo)
    return cpuinfo

def get_cpu_info2(file_path='/proc/cpuinfo'):
    """Get System's CPU/s specifications as a dict"""
    cpuinfo = {}
    procnum = str(0)
    cpuinfo[procnum] = {}
    with open(file_path) as fd:
        for line in fd:
            try:
                key, value = extract_values(line)
                if key != 'processor':
                    cpuinfo[procnum][key] = value
            except ValueError:
                # empty line => next processor
                procnum = str(int(procnum)+1)
                cpuinfo[procnum] = {}
    # extra space at the end of input => we need to delete empty processor
    del cpuinfo[procnum]
    cpuinfo['real'], cpuinfo['cores'], cpuinfo['total'] = get_totals(cpuinfo)
    return cpuinfo

def extract_values(line):
    """"Normalize lines taken from /proc/cpuinfo"""

    key, value = line.split(':')
    key, value = key.strip(), value.strip()
    key = key.replace(' ', '_')
    # values as lists
    if key.lower() in ('flags', 'bugs'):
        value = value.split()
    return key.lower(), value

def to_bytes(_dict, enc='utf-8'):
    """Convert dict to byte-json"""

    return bytes(json.dumps(_dict), enc)


class HTTPHandler(BaseHTTPRequestHandler):
    """Simple GET-only HTTP Server"""

    cpuinfo = to_bytes(get_cpu_info2())

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
            
        
def run(port, server_class=HTTPServer, handler_class=HTTPHandler):
    """Main loop"""

    httpd = server_class(('', port), handler_class)
    print(f'Server started at port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = DEFAULT_PORT
    run(port)

# END
