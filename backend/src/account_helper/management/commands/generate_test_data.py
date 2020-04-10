from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from account_helper.models import Realm


class Command(BaseCommand):
    help = 'Generate test data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            admin = User.objects.create_superuser(username="admin", password="2malDrei")
            admin.is_superuser = True
            admin.is_active = True
            admin.is_staff = True
            admin.is_admin = True
            admin.save()
        except:
            admin = User.objects.get(username="admin")

        Realm.objects.create(name="WIAI", ldap_base_dn="ou=wiai,ou=fachschaften,dc=test,dc=de", email="test@root.de")
        Realm.objects.create(name="SOWI", ldap_base_dn="ou=sowi,ou=fachschaften,dc=test,dc=de")
        Realm.objects.create(name="HUWI", ldap_base_dn="ou=huwi,ou=fachschaften,dc=test,dc=de")
