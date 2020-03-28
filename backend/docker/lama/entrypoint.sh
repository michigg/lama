#!/bin/sh
echo "-------- make migrations --------"
python3 /lama/manage.py makemigrations account_helper
echo "-------- migrate --------"
python3 /lama/manage.py migrate
echo "-------- start test --------"
python3 /lama/manage.py test
