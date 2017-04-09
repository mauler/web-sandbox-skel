FROM python:3

RUN mkdir -v /Src

VOLUME "/Src"

WORKDIR /Src

RUN pwd

ADD requirements.txt /Src/requirements.txt

RUN pip3 install -r requirements.txt
