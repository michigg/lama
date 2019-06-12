from django.shortcuts import render

from account_manager.models import LdapUser, LdapGroup


def render_user_detail_view(request, realm, ldap_user):
    user_wrapper = LdapUser.get_extended_user(ldap_user)
    LdapGroup.base_dn = LdapGroup.ROOT_DN
    groups = LdapGroup.objects.filter(members=ldap_user.dn)
    return render(request, 'user/user_detail.jinja2', {'user': user_wrapper, 'groups': groups, 'realm': realm})