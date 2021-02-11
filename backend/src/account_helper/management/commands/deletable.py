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
            '-d', '--delete',
            action='store_true',
            help='Delete users which deletion time is lower than the current date',
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='Return an json encoded String',
        )
        parser.add_argument(
            '-a', '--all',
            action='store_true',
            help='Delete all marked user, --delete is required',
        )

        parser.add_argument(
            '--fduser',
            type=str,
            help='Force delete specified user',
        )

    @staticmethod
    def get_json(deletable: DeletedUser):
        return {'ldap_dn': deletable.ldap_dn, 'username': deletable.user.username}

    def handle(self, *args, **options):
        if options['all'] and not options['fduser']:
            deletables = DeletedUser.objects.all()
        elif not options['all'] and options['fduser']:
            try:
                deletable = DeletedUser.objects.get(user__username=options['fduser'])
                LdapUser.base_dn = LdapUser.ROOT_DN
                ldap_user = LdapUser.objects.get(dn=deletable.ldap_dn)
                ldap_user.delete_complete()
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with the username {options['fduser']} not found."))
            return
        elif not options['all'] and not options['fduser']:
            deletables = DeletedUser.objects.filter(deletion_date__lte=timezone.now())
        else:
            self.stdout.write(self.style.ERROR(f"The parameter combination is not processable"))
            return

        output = ""
        if options['json']:
            json_output = {'deletables': [self.get_json(deletable) for deletable in deletables]}
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
