FROM python:3.7.3-alpine

WORKDIR /opt/cpuinfo

ADD . .
ENTRYPOINT ["/opt/cpuinfo/cpuinfo.py"]
CMD ["8080"]
