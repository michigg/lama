# Create your models here.
import logging
import os
import re
from datetime import datetime, timedelta
from typing import List

from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from django.db.models import Q
from ldap import NO_SUCH_OBJECT, ALREADY_EXISTS
from ldapdb.models import fields as ldap_fields
from ldapdb.models.base import Model

from account_helper.models import DeletedUser, Realm
from account_manager.utils.dbldap import get_filterstr
from account_manager.utils.mail_utils import send_welcome_mail

logger = logging.getLogger(__name__)

import ldap


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
        ldap_user, user = LdapUser.create_with_django_user(realm, username, email)
        send_welcome_mail(domain, email, protocol, realm, user)
        return ldap_user

    @staticmethod
    def create_with_django_user(realm, username, email, password=None):
        if not LdapUser.is_user_duplicate(username):
            LdapUser.base_dn = f'ou=people, {realm.ldap_base_dn}'
            # TODO: rewrite
            if password:
                ldap_user = LdapUser.objects.create(username=username, email=email, first_name=" ", last_name=" ",
                                                    password=password)
            else:
                ldap_user = LdapUser.objects.create(username=username, email=email, first_name=" ", last_name=" ")
            if password:
                user, _ = User.objects.get_or_create(username=username, email=email, password=password)
            else:
                user, _ = User.objects.get_or_create(username=username, email=email)
            return ldap_user, user
        else:
            raise ALREADY_EXISTS('User already exists')

    @staticmethod
    def get_extended_user(ldap_user):
        wrapper = {'user': ldap_user}
        try:
            wrapper['deleted_user'] = DeletedUser.objects.get(ldap_dn=ldap_user.dn)
        except ObjectDoesNotExist:
            wrapper['deleted_user'] = {}
        try:
            django_user = User.objects.get(username=ldap_user.username)
            wrapper['active'] = True if django_user.last_login else False
        except ObjectDoesNotExist:
            wrapper['active'] = False
        return wrapper

    @staticmethod
    def password_reset(user, raw_password):
        LdapUser.base_dn = LdapUser.ROOT_DN
        ldap_user = LdapUser.objects.get(username=user.username)
        ldap_user.password = raw_password
        LdapUser.base_dn = re.compile('(uid=[a-zA-Z0-9_-]*),(.*)').match(ldap_user.dn).group(2)
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
    def is_user_duplicate(username: str):
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

    def get_users_realm_base_dn(self):
        return re.compile('(uid=[a-zA-Z0-9_-]*),(ou=[a-zA-Z_-]*),(.*)').match(self.dn).group(3)

    @staticmethod
    def get_user(username: str, realm: Realm = None):
        LdapUser.base_dn = f'ou=people, {realm.ldap_base_dn}' if realm else LdapUser.ROOT_DN
        try:
            return LdapUser.objects.get(username=username)
        except Exception as e:
            return None

    @staticmethod
    def get_user_by_dn(dn: str, realm: Realm = None):
        LdapUser.base_dn = f'ou=people, {realm.ldap_base_dn}' if realm else LdapUser.ROOT_DN
        try:
            return LdapUser.objects.get(dn=dn)
        except Exception as e:
            return None

    @staticmethod
    def get_users(realm: Realm = None):
        LdapUser.base_dn = f'ou=people, {realm.ldap_base_dn}' if realm else LdapUser.ROOT_DN
        try:
            return LdapUser.objects.all()
        except Exception as e:
            return None

    @staticmethod
    def get_inactive_users(realm: Realm = None):
        LdapUser.base_dn = realm.ldap_base_dn if realm else LdapUser.ROOT_DN
        last_semester = datetime.now() - timedelta(days=182)
        return (LdapUser.objects.filter(last_login__lte=last_semester) | LdapUser.objects.exclude(
            last_login__lte=datetime.now() + timedelta(days=1)))

    def get_django_user(self):
        try:
            return User.objects.get(username=self.username)
        except ObjectDoesNotExist:
            return None

    def get_deletable(self):
        try:
            return DeletedUser.objects.get(ldap_dn=self.dn)
        except ObjectDoesNotExist:
            return None

    def delete_complete(self):
        django_user = self.get_django_user()
        deletable_user = self.get_deletable()
        LdapGroup.remove_user_from_groups(self.dn)
        self.delete()
        if django_user:
            django_user.delete()
        if deletable_user:
            deletable_user.delete()

    @staticmethod
    def set_root_dn(realm):
        LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'


class LdapGroup(Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    ROOT_DN = os.environ.get('LDAP_USER_ENTRY', 'dc=test,dc=de')
    base_dn = ROOT_DN
    object_classes = ['groupOfNames']

    name = ldap_fields.CharField(db_column='cn', max_length=200, primary_key=True)
    description = ldap_fields.CharField(db_column='description', max_length=1024)
    members = ldap_fields.ListField(db_column='member')

    @staticmethod
    def get_user_groups(realm: Realm, ldap_user: LdapUser):
        LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
        LdapGroup.base_dn = LdapGroup.ROOT_DN
        return LdapGroup.objects.filter(members=ldap_user.dn)

    @staticmethod
    def add_user_to_groups(ldap_user: LdapUser, ldap_groups: List):
        for ldap_group in ldap_groups:
            ldap_group.members.append(ldap_user.dn)
            ldap_group.save()

    @staticmethod
    def remove_user_from_groups(ldap_user_dn, user_groups=None):
        if not user_groups:
            LdapGroup.base_dn = LdapGroup.ROOT_DN
            user_groups = LdapGroup.objects.filter(members__contains=ldap_user_dn)
        for group in user_groups:
            LdapGroup.base_dn = re.compile('cn=([a-zA-Z0-9_-]*),(ou=[a-zA-Z_]*.*)').match(group.dn).group(2)
            group.members.remove(ldap_user_dn)
            group.save()

    def get_django_group(self):
        django_group, _ = Group.objects.get_or_create(name=self.name)
        return django_group

    @staticmethod
    def get_group(group_name: str, realm: Realm = None):
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}' if realm else LdapGroup.ROOT_DN
        try:
            return LdapGroup.objects.get(name=group_name)
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def get_groups(realm: Realm = None):
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}' if realm else LdapGroup.ROOT_DN
        try:
            return LdapGroup.objects.all()
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def set_root_dn(realm):
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
