# LAMa (Ldap Account Manager)
LAMa wurde für die Studierendenvertretung der Universität Bamberg entwickelt, um ein einfache Accountverwaltung der StuVe Accounts zu gewährleisten. Es soll eine einfachere Alternative zu dem Accountmangementool Keycloak bieten. Das Tool baut auf dem Pythonframework django auf und verwendet die Pakete `django-auth-ldap`, `django-ldapdb` für die Verbindung mit ldap.

## Developer Setup
1. repo klonen
2. `docker-compose build`
3. `docker-compose up -d`
4. `docker-compose exec lama sh`
    1. `python manage.py makemigrations account_helper`
    2. `python manage.py migrate`
    3. `python manage.py createsuperuser`
5. `docker-compose logs -f lama` (Anzeige der server logs)  

Für die Verwaltung von LDAP wurde ein phpldapadmin gestartet. Dieses ist unter `ldap.localhost` erreichbar. Das voreingestellte Passwort lautet `secret`.

LAMa ist unter `lama.localhost` erreichbar.

Für das Frontendmanagement wird ein Traefik gestartet, der unter `traefik.localhost` erreichbar ist.

Nach dem initialen Setup sind nur noch Schritte 3, 5 nötig.

## Production Setup
- TODO


## Special thanks
Ich möchte mich vor allem bei @cklug und @mhofmann bedanken für die Unterstützung bei diesem Projekt. 
