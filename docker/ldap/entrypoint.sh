#!/bin/sh
slapadd -l /etc/openldap/start.ldif
chown ldap:ldap -R /var/lib/openldap
slapd -u ldap -g ldap -d 32768

