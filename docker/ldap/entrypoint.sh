#!/bin/sh
chown ldap:ldap -R /var/lib/openldap
slapadd -l /etc/openldap/start.ldif
slapd -u ldap -g ldap -d 32768

