from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import models
from django.utils import timezone

# Create your models here.
from account_helper.validators import validate_ldap_base_dn


class Realm(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200)
    admin_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True, related_name='admin_groups')
    default_group = models.ForeignKey(Group, models.PROTECT, blank=True, null=True, related_name='default_groups')
    ldap_base_dn = models.CharField(max_length=400, unique=True, validators=[validate_ldap_base_dn])

    def delete(self, using=None, keep_parents=False):
        from account_manager.models import LdapUser
        from account_manager.models import LdapGroup
        from _ldap import LDAPError
        try:
            ldap_users = LdapUser.get_users(self)
            ldap_usernames = [user.username for user in ldap_users]
            ldap_groups = LdapGroup.get_groups(self)
            ldap_groupnames = [group.name for group in ldap_groups]
            django_user = User.objects.filter(username__contains=ldap_usernames)
            django_groups = Group.objects.filter(name__contains=ldap_groupnames)
            django_user.delete()
            django_groups.delete()
            ldap_users.delete()
            ldap_groups.delete()
        except LDAPError:
            # TODO: Save delete
            pass
        return super().delete(using, keep_parents)

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
