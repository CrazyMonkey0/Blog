#!/bin/sh
python manage.py makemigrations
python manage.py migrate
# remove it after image build 
python manage.py loaddata whole.json
exec "$@"
