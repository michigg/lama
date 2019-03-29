# Create your models here.
from django.db import models
from ldapdb.models import fields as ldap_fields
from ldapdb.models.base import Model


class LdapUser(Model):
    """
    Class for representing an LDAP user entry.
    """
    # LDAP meta-data
    ROOT_DN = "dc=stuve,dc=de"
    base_dn = "dc=stuve,dc=de"
    object_classes = ['inetOrgPerson']
    last_modified = ldap_fields.DateTimeField(db_column='modifyTimestamp', blank=True)

    # inetOrgPerson
    username = ldap_fields.CharField(db_column='uid', primary_key=True)
    # rdn = ''
    password = ldap_fields.CharField(db_column='userPassword')
    first_name = ldap_fields.CharField(db_column='cn', blank=True)
    last_name = ldap_fields.CharField(db_column='sn', blank=True)
    email = ldap_fields.CharField(db_column='mail')
    phone = ldap_fields.CharField(db_column='telephoneNumber', blank=True)
    mobile_phone = ldap_fields.CharField(db_column='mobile', blank=True)
    photo = ldap_fields.ImageField(db_column='jpegPhoto')

    # def __init__(self, *args, **kwargs):
    #     self.rdn = kwargs.get('rdn', None)
    #     if self.rdn:
    #         del kwargs['rdn']
    #     super().__init__(*args, **kwargs)
    #
    # def build_dn(self):
    #     """
    #     Build the Distinguished Name for this entry.
    #     """
    #     return "%s,%s,%s" % (self.build_rdn(), self.rdn, self.base_dn)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.full_name


class LdapGroup(Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    ROOT_DN = "dc=stuve,dc=de"
    base_dn = "dc=stuve,dc=de"
    object_classes = ['groupOfNames']

    # posixGroup attributes
    # rdn = ''
    name = ldap_fields.CharField(db_column='cn', max_length=200, primary_key=True)
    members = ldap_fields.ListField(db_column='member')

    # def __init__(self, *args, **kwargs):
    #     self.rdn = kwargs.get('rdn', None)
    #     if self.rdn:
    #         del kwargs['rdn']
    #     super().__init__(*args, **kwargs)
    #
    # def build_dn(self):
    #     """
    #     Build the Distinguished Name for this entry.
    #     """
    #     return "%s,%s,%s" % (self.build_rdn(), self.rdn, self.base_dn)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
