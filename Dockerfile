# pull official base image
FROM python:3.9.5-alpine

# set work directory
WORKDIR /usr/src/main

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && apk add --no-cache postgresql-client \
    && pip install psycopg2 ruamel.yaml.clib  \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/main/requirements.txt
RUN pip install -r /usr/src/main/requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/main/entrypoint.sh

# copy project
COPY . /usr/src/main/

# run entrypoint.sh
ENTRYPOINT ["sh", "/usr/src/main/entrypoint.sh"]