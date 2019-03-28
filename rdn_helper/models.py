from django.db import models


# Create your models here.
class LdapUserRDN(models.Model):
    rdn = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.rdn


class LdapGroupRDN(models.Model):
    rdn = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.rdn
