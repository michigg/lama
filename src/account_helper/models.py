from django.contrib.auth.models import Group, User
from django.db import models


# Create your models here.
class Realm(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200)
    admin_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True, related_name='admin_groups')
    default_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True, related_name='default_groups')
    ldap_base_dn = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return f'{self.name} - {self.ldap_base_dn}'


# class DeletedUser(models.Model):
#     deletion_date = models.DateField(auto_now=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user.username} - {self.deletion_date}'
