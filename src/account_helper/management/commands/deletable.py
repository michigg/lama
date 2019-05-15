from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from account_manager.models import LdapGroup, LdapUser
from account_helper.models import DeletedUser
from django.utils import timezone
from django.core import serializers
import json


class Command(BaseCommand):
    help = 'Get and delete the deleted marked users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete poll instead of closing it',
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='Return an json encoded String',
        )

    def handle(self, *args, **options):
        deletables = DeletedUser.objects.filter(deletion_date__lte=timezone.now() + timezone.timedelta(+16))
        output = ""
        if options['json']:
            django_serialized = serializers.serialize('json', deletables)
            output = json.dumps({'deletables': json.loads(django_serialized)})
        else:
            for user in deletables:
                output += f'{user}\n'

        if options['delete']:
            for user in deletables:
                # LdapGroup.base_dn = LdapGroup.ROOT_DN
                # user_groups = LdapGroup.objects.filter(members__contains=user.ldap_dn)
                LdapUser.base_dn = LdapUser.ROOT_DN
                ldap_user = LdapUser.objects.get(dn=user.ldap_dn)
                LdapGroup.remove_user_from_groups(ldap_user)
                ldap_user.delete()
                try:
                    user.user.delete()
                    user.delete()
                except ObjectDoesNotExist:
                    pass
            if not options['json']:
                output += '\nSuccessfully deleted all listed users'
        self.stdout.write(self.style.SUCCESS(output))
