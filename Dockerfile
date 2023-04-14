FROM python:3.8.1-slim-buster
LABEL maintainer Genopaths Africa<support@genopaths.africa>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt -y install software-properties-common && add-apt-repository ppa:deadsnakes/ppa -y 

RUN apt-get install -y python-pip python-virtualenv netcat git wget zlib1g-dev libffi-dev \
    libssl-dev

# Setup flask application
RUN mkdir -p /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

WORKDIR /app

EXPOSE 8181

# Start gunicorn
CMD ["gunicorn", "--config", "/app/gunicorn_config.py", "wsgi:app"]
