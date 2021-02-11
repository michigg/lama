FROM alpine:3.10

ADD ["docker/lama/requirements.txt", "/requirements.txt"]
RUN apk upgrade --update && \
	apk add --update python3 build-base openldap-dev python3-dev py3-psycopg2 && \
	pip3 install -r /requirements.txt && rm /requirements.txt
WORKDIR /lama
EXPOSE 80

ENTRYPOINT ["python3", "manage.py"]
ADD ["src", "/lama"]

RUN rm -r /lama/account_manager/tests

CMD ["runserver", "0.0.0.0:80"]
