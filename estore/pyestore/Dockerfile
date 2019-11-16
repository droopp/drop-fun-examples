FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python && apt-get install -y python-pip
RUN useradd drop
RUN pip install gevent

COPY ./*.py /home/drop/
