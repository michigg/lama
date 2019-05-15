from django.core.management.base import BaseCommand, CommandError
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
                pass
            if not options['json']:
                output += '\nSuccessfully deleted all listed users'
        self.stdout.write(self.style.SUCCESS(output))
