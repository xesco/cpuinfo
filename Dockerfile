FROM python:3.7.3-alpine

EXPOSE 8080
WORKDIR /opt/cpuinfo

ADD cpuinfo.py .
ENTRYPOINT ["/opt/cpuinfo/cpuinfo.py"]
CMD ["8080"]
