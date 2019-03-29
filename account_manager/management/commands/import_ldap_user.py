from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from account_manager.models import UserProfile
import ldap
import core.settings as settings

LDAP_CONFIGS = [(settings.AUTH_LDAP_1_SERVER_URI, settings.AUTH_LDAP_1_USER_DN_TEMPLATE),
                (settings.AUTH_LDAP_2_SERVER_URI, settings.AUTH_LDAP_2_USER_DN_TEMPLATE)]


class Command(BaseCommand):
    help = 'Syncs LDAP users with Django DB'

    def handle(self, *args, **options):
        for ldap_config in LDAP_CONFIGS:
            ldap_server = ldap.initialize(ldap_config[0])
            ldap_dn = ldap_config[1].split(',')
            ldap_dn.pop(0)
            ldap_dn = ",".join(ldap_dn)
            results = ldap_server.search_s(ldap_dn, ldap.SCOPE_SUBTREE,
                                           "(objectClass=inetOrgPerson)")

            total_created = 0
            total = 0

            for a, r in results:
                username = r['uid'][0].decode('utf-8')  # returns bytes by default so we need to decode to string.
                first_name = r['cn'][0].decode('utf-8')
                last_name = r['sn'][0].decode('utf-8')
                # email = r['mail'][0].decode('utf-8')

                # Update the user -- this allows for name changes etc, using username as the key.
                user, created = User.objects.update_or_create(username=username,
                                                              defaults={'first_name': first_name,
                                                                        'last_name': last_name})

                total += 1

                if created:
                    # Set an unusable password -- django-auth-ldap handles this, anyway.
                    user.set_unusable_password()
                    user.save()
                    total_created += 1

            self.stdout.write(self.style.SUCCESS('Found {} user(s), {} new.'.format(total, total_created)))
