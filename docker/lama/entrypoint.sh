#!/bin/sh
python3 /lama/manage.py makemigrations account_helper && \
python3 /lama/manage.py migrate && \
python3 /lama/manage.py runserver 0.0.0.0:80
