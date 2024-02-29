#!/bin/bash

set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
#python manage.py createsuperuser --noinput

uwsgi --strict --ini /opt/app/uwsgi.ini
