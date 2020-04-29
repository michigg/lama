from django.contrib.auth.models import User, Permission
from django.core.management.base import BaseCommand

from account_helper.models import Realm
from account_manager.models import LdapGroup, LdapUser


class Command(BaseCommand):
    help = 'Generate test data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            admin = User.objects.create_superuser(username="admin", email="admin@admin.de", password="2malDrei")
            admin.is_superuser = True
            admin.is_active = True
            admin.is_staff = True
            admin.is_admin = True
            admin.save()
        except:
            admin = User.objects.get(username="admin")

        wiai = Realm.objects.create(name="WIAI", ldap_base_dn="ou=wiai,ou=fachschaften,dc=test,dc=de",
                                    email="test@root.de")
        Realm.objects.create(name="SOWI", ldap_base_dn="ou=sowi,ou=fachschaften,dc=test,dc=de")
        Realm.objects.create(name="HUWI", ldap_base_dn="ou=huwi,ou=fachschaften,dc=test,dc=de")

        ldap_user, user = LdapUser.create_with_django_user(realm=wiai,
                                                           username="test",
                                                           email="test@test.de",
                                                           password="2malDrei")
        ldap_group = LdapGroup.full_create(wiai, name="TestGroup", members=[ldap_user.dn])
        django_group = ldap_group.get_django_group()

        permission = Permission.objects.get(codename="add_deleteduser")
        django_group.permissions.add(permission)
        django_group.save()
