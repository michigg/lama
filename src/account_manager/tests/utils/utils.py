import logging

from _ldap import ALREADY_EXISTS
from django.contrib.auth.models import User

from account_helper.models import Realm
from account_manager.models import LdapUser, LdapGroup

PASSWORD = "12345678"


def get_realm(id: int, email=True):
    realm, _ = Realm.objects.get_or_create(name=f"test_realm_{id}",
                                           ldap_base_dn=f"ou=test_{id},dc=test,dc=de",
                                           email=f"test_{id}.realm@test.de" if email else "")
    return realm


def get_user(id: int, realm: Realm, admin=False, multiple_admin=False, super_admin=False):
    LdapUser.set_root_dn(realm=realm)
    username = f"test_user_{id}"
    email = f"test_user_{id}t@test.de"
    first_name = f"test_{id}"
    last_name = f"musterstudierender_{id}"
    if admin:
        username = f"test_admin_user_{id}"
        email = f"test_admin_user_{id}t@test.de"
        first_name = f"test_admin_{id}"
        last_name = f"musterstudierender_admin_{id}"
    if multiple_admin:
        username = f"test_multiple_admin_user_{id}"
        email = f"test_multiple_admin_user_{id}t@test.de"
        first_name = f"test_multiple_admin_{id}"
        last_name = f"musterstudierender_multiple_admin_{id}"
    if super_admin:
        username = f"test_super_user_{id}"
        email = f"test_super_user_{id}t@test.de"
        first_name = f"test_super_user_{id}"
        last_name = f"musterstudierender_super_user_{id}"
    try:
        ldap_user, _ = LdapUser.objects.get_or_create(username=username,
                                                      email=email,
                                                      password=PASSWORD,
                                                      first_name=first_name,
                                                      last_name=last_name)
        User.objects.create(username=username, email=email, password=PASSWORD, first_name=first_name,
                            last_name=last_name)
    except ALREADY_EXISTS:
        ldap_user = LdapUser.objects.get(username=username, )

    return ldap_user


def get_group(id: int, realm: Realm, ldap_groups):
    LdapGroup.set_root_dn(realm)
    ldap_group_dns = [ldap_group.dn for ldap_group in ldap_groups]
    try:
        ldap_group, _ = LdapGroup.objects.get_or_create(name=f"test_group_{id}", members=ldap_group_dns)
    except ALREADY_EXISTS:
        ldap_group = LdapGroup.objects.get(name=f"test_group_{id}", )
    return ldap_group


def get_password():
    return PASSWORD


def clear_realm_user(realm: Realm):
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    for ldap_user in LdapUser.objects.all():
        ldap_user.delete()


def clear_realm_group(realm: Realm):
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    for ldap_group in LdapGroup.objects.all():
        ldap_group.delete()
