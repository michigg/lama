from django.core.management.base import BaseCommand
from src.account_helper import LdapGroupRDN, LdapUserRDN

LDAP_OUS = ['ou=fs_wiai,ou=fachschaften', 'ou=fs_sowi,ou=fachschaften']


class Command(BaseCommand):
    help = 'Load Possible User Dns in LDAP'

    def handle(self, *args, **options):
        added_groups_rdn = 0
        added_user_rdn = 0
        for ou in LDAP_OUS:
            _, group_created = LdapGroupRDN.objects.get_or_create(rdn=f'ou=groups,{ou}')
            _, user_created = LdapUserRDN.objects.get_or_create(rdn=f'ou=people,{ou}')
            if group_created:
                added_groups_rdn += 1
            if user_created:
                added_user_rdn += 1

        print(f'Added {added_user_rdn} user rdns\nAdded {added_groups_rdn} group rdns')
