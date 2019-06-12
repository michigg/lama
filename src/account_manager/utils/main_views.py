from django.shortcuts import render

from account_helper.models import Realm
from account_manager.models import LdapUser, LdapGroup


# def render_realm_detail_page(realm_id, request, notice=""):
#     realm = Realm.objects.get(id=realm_id)
#     ldap_admin_group, ldap_default_group = get_default_admin_group(realm)
#     LdapUser.base_dn = realm.ldap_base_dn
#     inactive_users = LdapUser.get_inactive_users().count()
#     return render(request, 'realm/realm_detailed.jinja2',
#                   {'realm': realm, 'ldap_admin_group': ldap_admin_group, 'ldap_default_group': ldap_default_group,
#                    'inactive_user_count': inactive_users, 'users_count': LdapUser.objects.all().count(),
#                    'notice': notice})


def render_realm_detail_view(request, realm_id, success_headline=None, success_text=None, error_headline=None,
                             error_text=None, status_code=200):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm.ldap_base_dn
    inactive_users = LdapUser.get_inactive_users().count()
    ldap_admin_group, ldap_default_group = get_default_admin_group(realm)
    return render(request, 'realm/realm_detailed.jinja2',
                  {'realm': realm,
                   'ldap_admin_group': ldap_admin_group,
                   'ldap_default_group': ldap_default_group,
                   'inactive_user_count': inactive_users,
                   'users_count': LdapUser.objects.all().count(),
                   'success_headline': success_headline,
                   'success_text': success_text,
                   'error_headline': error_headline,
                   'error_text': error_text}, status=status_code)


def get_default_admin_group(realm):
    ldap_admin_group = None
    ldap_default_group = None
    if realm.admin_group:
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
        ldap_admin_group = LdapGroup.objects.get(name=realm.admin_group.name)
    if realm.default_group:
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
        ldap_default_group = LdapGroup.objects.get(name=realm.default_group.name)
    return ldap_admin_group, ldap_default_group


def render_permission_denied_view(request):
    return render(request, 'permission_denied.jinja2', {}, status=403)
