#!/bin/bash

apt-get install -y libpq-dev
pip install -r requirements.txt
python manage.py collectstatic --noinput
