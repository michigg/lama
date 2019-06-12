from django.shortcuts import render

from account_helper.models import Realm
from account_manager.main_views import get_default_admin_group
from account_manager.models import LdapUser


def render_realm_detail_page(realm_id, request, notice=""):
    realm = Realm.objects.get(id=realm_id)
    ldap_admin_group, ldap_default_group = get_default_admin_group(realm)
    LdapUser.base_dn = realm.ldap_base_dn
    inactive_users = LdapUser.get_inactive_users().count()
    return render(request, 'realm/realm_detailed.jinja2',
                  {'realm': realm, 'ldap_admin_group': ldap_admin_group, 'ldap_default_group': ldap_default_group,
                   'inactive_user_count': inactive_users, 'users_count': LdapUser.objects.all().count(),
                   'notice': notice})