FROM alpine:3.7

RUN apk add --update --no-cache phpldapadmin apache2 php5-apache2
COPY ./httpd.conf /etc/apache2/httpd.conf
COPY ./phpldapadmin_conf.php /etc/phpldapadmin/config.php
RUN sed -i 's!/run/apache2/httpd.pid!/tmp/apache2.pid!' /etc/apache2/conf.d/mpm.conf

EXPOSE 80

ENTRYPOINT ["/usr/sbin/httpd", "-D", "FOREGROUND"]
