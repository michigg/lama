FROM alpine:3.9
ADD ["requirements.txt", "/requirements.txt"]
RUN apk upgrade --update && \
	apk add --update python3 build-base openldap-dev python3-dev py3-psycopg2 && \
	pip3 install -r /requirements.txt && rm /requirements.txt
WORKDIR /lama
EXPOSE 80

ENTRYPOINT ["python3", "manage.py"]
ADD ["src", "/lama"]
CMD ["runserver", "0.0.0.0:80"]
