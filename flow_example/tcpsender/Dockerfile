FROM ubuntu:16.04

RUN apt-get update && apt-get install -y netcat
RUN useradd drop

COPY ./tcpsender /home/drop/
