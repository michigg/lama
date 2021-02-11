#!/bin/sh
echo "-------- make migrations --------"
python3 /lama/manage.py makemigrations account_helper
echo "-------- migrate --------"
python3 /lama/manage.py migrate
echo "-------- generate test data --------"
python3 /lama/manage.py generate_test_data
echo "-------- start server --------"
python3 /lama/manage.py runserver 0.0.0.0:80
