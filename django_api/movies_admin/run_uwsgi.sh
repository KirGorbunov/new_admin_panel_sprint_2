#!/bin/bash

set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
#python manage.py createsuperuser --noinput
python /opt/sqlite_to_postgres/load_data.py

uwsgi --strict --ini /opt/app/uwsgi.ini
