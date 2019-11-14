
![Drone (self-hosted)](https://img.shields.io/drone/build/michigg/lama?server=https%3A%2F%2Fdrone.github.michigg.de&style=for-the-badge)
[![Contributors](https://img.shields.io/github/contributors/michigg/lama.svg?style=for-the-badge)](https://github.com/michigg/lama)
[![Forks](https://img.shields.io/github/forks/michigg/lama.svg?style=for-the-badge)](https://github.com/michigg/lama)
[![Stars](https://img.shields.io/github/stars/michigg/lama.svg?style=for-the-badge)](https://github.com/michigg/lama)
[![Issues](https://img.shields.io/github/issues/michigg/lama.svg?style=for-the-badge)](https://github.com/michigg/lama)
[![License](https://img.shields.io/github/license/michigg/lama.svg?style=for-the-badge)](https://github.com/michigg/lama)

# LAMa (Ldap Account Manager)
LAMa was developed for the student representation of the University of Bamberg in order to guarantee a simple account administration of the StuVe accounts. It should offer a simpler alternative to the Keycloak account management tool.
The tool is based on the Python framework django and uses the packages `django-auth-ldap`, `django-ldapdb` to connect to ldap.

## Developer Setup
1. clone or unzip repo
2. `docker-compose build`
3. `docker-compose run ldap sh`
4. `chown ldap:ldap -R /var/lib/openldap/`
5. `docker-compose up -d`
6. `docker-compose exec lama sh`
    1. `python3 manage.py makemigrations account_helper`
    2. `python3 manage.py migrate`
    3. `python3 manage.py createsuperuser`
7. `docker-compose logs -f lama` (Display server logs)  

phpldapadmin was started to manage LDAP. This is available under `localhost:8080`. The default password is `secret`.

LAMa can be reached under `localhost:8888`.

After the initial setup only steps 3, 5 are necessary.

## Production Setup
- TODO


## Used Libraries
### Frontend
- Bootstrap4 (MIT)
- jquery (MIT)
- dataTables (MIT)

### Backend
- Django (BSD)
- django-auth-ldap (BSD 2 Clause)
- django-ldapdb (BSD 2 Clause)
- jinja2 (BSD 3 Clause)
