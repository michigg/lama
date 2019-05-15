# Create your models here.
import logging
import os
import re
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from ldap import NO_SUCH_OBJECT, ALREADY_EXISTS
from ldapdb.models import fields as ldap_fields
from ldapdb.models.base import Model

from account_manager.utils.mail_utils import send_welcome_mail

logger = logging.getLogger(__name__)


class LdapUser(Model):
    """
    Class for representing an LDAP user entry.
    """
    # LDAP meta-data
    ROOT_DN = os.environ.get('LDAP_USER_ENTRY', 'dc=test,dc=de')
    base_dn = ROOT_DN
    object_classes = ['inetOrgPerson']
    # last_modified = ldap_fields.DateTimeField(db_column='modifyTimestamp', blank=True)

    # inetOrgPerson
    username = ldap_fields.CharField(db_column='uid', primary_key=True)
    display_name = ldap_fields.CharField(db_column='displayName', blank=True)
    password = ldap_fields.CharField(db_column='userPassword')
    first_name = ldap_fields.CharField(db_column='cn', blank=True)
    last_name = ldap_fields.CharField(db_column='sn', blank=True)
    email = ldap_fields.CharField(db_column='mail')
    phone = ldap_fields.CharField(db_column='telephoneNumber', blank=True)
    mobile_phone = ldap_fields.CharField(db_column='mobile', blank=True)
    photo = ldap_fields.ImageField(db_column='photo')
    last_login = ldap_fields.DateTimeField(db_column='authTimestamp', blank=True)

    # photo = ldap_fields.ImageField(db_column='jpegPhoto')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.full_name

    @staticmethod
    def create_with_django_user_creation_and_welcome_mail(realm, protocol, domain, username, email):
        if not LdapUser.is_user_duplicate(username):
            LdapUser.base_dn = f'ou=people, {realm.ldap_base_dn}'
            ldap_user = LdapUser.objects.create(username=username, email=email, first_name=" ", last_name=" ")
            user, _ = User.objects.get_or_create(username=username, email=email)
            send_welcome_mail(domain, email, protocol, realm, user)
            return ldap_user
        else:
            raise ALREADY_EXISTS('User already exists')

    @staticmethod
    def password_reset(user, raw_password):
        LdapUser.base_dn = LdapUser.ROOT_DN
        ldap_user = LdapUser.objects.get(username=user.username)
        ldap_user.password = raw_password
        LdapUser.base_dn = re.compile('(uid=[a-zA-Z0-9_]*),(.*)').match(ldap_user.dn).group(2)
        ldap_user.save()

    @staticmethod
    def get_users_by_dn(realm, users):
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
        # logger.debug(users)
        users = [re.compile('uid=([a-zA-Z0-9_-]*),(ou=[a-zA-Z_]*),(.*)').match(user).group(1) for
                 user in users]
        query = Q(username=users.pop())
        for user in users:
            query = query | Q(username=user)
        LdapUser.base_dn = LdapUser.ROOT_DN
        return LdapUser.objects.filter(query)

    @staticmethod
    def is_user_duplicate(username):
        LdapUser.base_dn = LdapUser.ROOT_DN
        try:
            LdapUser.objects.get(username=username)
            return True
        except (NO_SUCH_OBJECT, ObjectDoesNotExist) as err:
            return False

    @staticmethod
    def is_active_user(ldap_user):
        try:
            django_user = User.objects.get(username=ldap_user.username)
            return django_user.last_login
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_user_active_marked(ldap_users):
        user_wrappers = []
        for user in ldap_users:
            if LdapUser.is_active_user(user):
                user_wrappers.append({'user': user, 'active': True})
            else:
                user_wrappers.append({'user': user, 'active': False})
        return user_wrappers

    @staticmethod
    def get_inactive_users():
        last_semester = datetime.now() - timedelta(days=182)
        return (LdapUser.objects.filter(last_login__lte=last_semester) | LdapUser.objects.exclude(
            last_login__lte=datetime.now() + timedelta(days=1)))


class LdapGroup(Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    ROOT_DN = os.environ.get('LDAP_USER_ENTRY', 'dc=test,dc=de')
    base_dn = ROOT_DN
    object_classes = ['groupOfNames']

    name = ldap_fields.CharField(db_column='cn', max_length=200, primary_key=True)
    members = ldap_fields.ListField(db_column='member')

    @staticmethod
    def get_user_groups(realm, user, group_base_dn):
        LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
        LdapGroup.base_dn = group_base_dn
        return LdapGroup.objects.filter(members=user.dn)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
