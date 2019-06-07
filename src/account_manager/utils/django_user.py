from django.contrib.auth.models import User


def update_dajngo_user(ldap_user):
    user, _ = User.objects.get_or_create(username=ldap_user.username)
    user.email = ldap_user.email
    user.save()
