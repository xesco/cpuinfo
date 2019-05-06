PROBLEM
=======
Create a Docker container which exposes a small web service on port
8080. This service should interpret the contents of the container's
cpuinfo to return a json payload in the following format. The web
service should be written in one of Ruby, Python, Go or Perl.

Example:

$ docker build -t challenge .
...
$ docker run -t -d -p 8080:8080 challenge
...
$ curl -s http://localhost:8080/ | jq
{
  "0": {
    "vendor_id": "IngenuineEntel",
    "family": "6",
    "model": "58",
    "model_name": "Entel(R) Core(TM) i6-2741QM CPU @ 8.70GHz",
    "stepping": "9",
    "mhz": "8693.860",
    "cache_size": "6144 KB",
    "physical_id": "0",
    "core_id": "0",
    "cores": "1",
    "flags": [
      "fpu",
      "vme",
      "etc"
    ]
  },
  "total": 1,
  "real": 1,
  "cores": 1
}

SOLUTION
========
- Get cpuinfo from /proc/cpuinfo
- Parse the file as json.
- Compute totals: total/real/cores
- Start a simple http server on port 8080 and serve the json

HOWTO
=====
$ make build
$ make run

REFERENCES
==========
http://doc.callmematthi.eu/static/webArticles/Understanding%20Linux%20_proc_cpuinfo.pdf
https://docs.python.org/3/library/http.server.html#module-http.server
https://docs.docker.com/engine/reference/builder/
