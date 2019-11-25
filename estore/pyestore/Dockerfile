FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python && apt-get install -y python-pip
RUN useradd drop
RUN pip install gevent
RUN pip install cassandra-driver

COPY ./*.py /home/drop/
