FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python && apt-get install -y python-pip
RUN useradd drop
RUN pip install gevent

COPY ./pyex_async.py /home/drop/
