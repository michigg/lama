import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils import timezone

from account_helper.models import DeletedUser
from account_manager.models import LdapGroup, LdapUser


class Command(BaseCommand):
    help = 'Get and delete the deleted marked users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete users which deletion time is lower than the current date',
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='Return an json encoded String',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Delete all marked user, --delete is required',
        )

    def handle(self, *args, **options):
        if options['all']:
            deletables = DeletedUser.objects.all()
        else:
            deletables = DeletedUser.objects.filter(deletion_date__lte=timezone.now())
        output = ""
        if options['json']:
            json_output = {'deletables': []}
            for deletable in deletables:
                json_output['deletables'].append({'ldap_dn': deletable.ldap_dn, 'username': deletable.user.username})
            output = json.dumps(json_output)
        else:
            for user in deletables:
                output += f'{user}\n'
        if options['delete']:
            LdapUser.base_dn = LdapUser.ROOT_DN
            for user in deletables:
                ldap_user = LdapUser.objects.get(dn=user.ldap_dn)
                ldap_user.delete_complete()
            if not options['json']:
                output += '\nSuccessfully deleted all listed users'
        if output:
            self.stdout.write(self.style.SUCCESS(output))
        else:
            for deletable in deletables:
                self.stdout.write(self.style.SUCCESS(deletable))
