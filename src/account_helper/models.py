from django.contrib.auth.models import Group, User
from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class Realm(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200)
    admin_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True, related_name='admin_groups')
    default_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True, related_name='default_groups')
    ldap_base_dn = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return f'{self.name} - {self.ldap_base_dn}'


def get_deletion_time():
    return timezone.now() + timezone.timedelta(settings.DELETION_WAIT_DAYS)


class DeletedUser(models.Model):
    deletion_marker_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ldap_dn = models.CharField(max_length=512, unique=True)
    deletion_date = models.DateField(default=get_deletion_time)

    def __str__(self):
        return f'{self.user.username} - {self.deletion_marker_date} - {self.deletion_date} - {self.ldap_dn}'
