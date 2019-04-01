FROM ubuntu:16.04

RUN apt-get update && apt-get install -y nodejs
RUN useradd drop

COPY ./word_count.js /home/drop/
