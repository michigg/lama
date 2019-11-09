from django.shortcuts import render

from account_helper.models import Realm
from account_manager.models import LdapUser, LdapGroup
from account_manager.utils.user_views import render_user_detail_view


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


def get_group_user_count_wrapper(realm):
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    return {'realm': realm, 'group_count': LdapGroup.objects.count(), 'user_count': LdapUser.objects.count()}


def get_users_home_view(request):
    django_user = request.user
    if django_user.is_superuser:
        realms = Realm.objects.order_by('name').all()
    else:
        realms = Realm.objects.filter(admin_group__user__username__contains=django_user.username).order_by('name')

    show_user = request.GET.get('show_user', False)
    if show_user or (len(realms) == 0 and not django_user.is_superuser):
        LdapUser.base_dn = LdapUser.ROOT_DN
        ldap_user = LdapUser.objects.get(username=django_user.username)
        realm = Realm.objects.get(ldap_base_dn=ldap_user.get_users_realm_base_dn())

        return render_user_detail_view(request, realm, ldap_user)
    elif len(realms) == 1 and not django_user.is_superuser:
        return render_realm_detail_view(request, realms[0].id)
    else:
        realm_wrappers = []
        for realm in realms:
            realm_wrappers.append(get_group_user_count_wrapper(realm))
        return render(request, 'realm/realm_home.jinja2', {'realms': realms, 'realm_wrappers': realm_wrappers})
