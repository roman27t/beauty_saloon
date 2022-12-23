FROM python:3.9.15-alpine

ENV PYTHONDONTWRITEBYTECODE 1 PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers
RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN apk del .tmp-build-deps

WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
