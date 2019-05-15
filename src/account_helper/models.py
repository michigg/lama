from django.contrib.auth.models import Group, User
from django.db import models
from django.utils import timezone


# Create your models here.
class Realm(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200)
    admin_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True, related_name='admin_groups')
    default_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True, related_name='default_groups')
    ldap_base_dn = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return f'{self.name} - {self.ldap_base_dn}'

