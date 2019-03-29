from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
class Realm(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=True, null=True)
    admin_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True)
    ldap_base_dn = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return f'{self.name} - {self.ldap_rdn_org}'


class LdapUserRDN(models.Model):
    rdn = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.rdn


class LdapGroupRDN(models.Model):
    rdn = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.rdn
