#!/bin/sh
echo "-------- make migrations --------"
python3 /lama/manage.py makemigrations account_helper
echo "-------- migrate --------"
python3 /lama/manage.py migrate
echo "-------- start test --------"
coverage run /lama/manage.py test
echo "-------- write test report --------"
coverage xml -i -o /coverage-reports/coverage.xml
