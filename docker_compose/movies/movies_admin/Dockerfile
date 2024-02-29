FROM python:3.12-bullseye

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini
COPY manage.py manage.py

RUN  mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && chmod +x run_uwsgi.sh \
     && apt update \
     && apt -y install gcc\
     && pip install --upgrade pip \
     && pip install -r requirements.txt

COPY ./config ./config
COPY ./movies ./movies

ENTRYPOINT ['./run_uwsgi.sh']