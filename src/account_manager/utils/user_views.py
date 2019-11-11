from _ldap import ALREADY_EXISTS
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render

from account_helper.models import Realm
from account_manager.forms import AddLDAPUserForm
from account_manager.models import LdapUser, LdapGroup


def render_user_detail_view(request, realm, ldap_user):
    user_wrapper = LdapUser.get_extended_user(ldap_user)
    LdapGroup.base_dn = LdapGroup.ROOT_DN
    groups = LdapGroup.objects.filter(members=ldap_user.dn)
    return render(request,
                  'user/user_detail.jinja2',
                  {
                      'user': user_wrapper,
                      'groups': groups,
                      'realm': realm,
                  }, )


def get_rendered_user_details(request, realm_id, user_dn, success_headline=None, success_text=None):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm.ldap_base_dn
    LdapGroup.base_dn = LdapGroup.ROOT_DN
    user = LdapUser.objects.get(dn=user_dn)
    user_wrapper = LdapUser.get_extended_user(user)
    groups = LdapGroup.objects.filter(members=user.dn)
    return render(request,
                  'user/realm_user_detail.jinja2',
                  {
                      'user': user_wrapper,
                      'groups': groups,
                      'realm': realm,
                      'success_headline': success_headline,
                      'success_text': success_text,
                  }, )


def get_realm_user_list(request, realm_id, status_code=200, success_headline="", success_text=""):
    realm = Realm.objects.get(id=realm_id)
    realm_users = LdapUser.get_users(realm=realm)
    user_wrappers = []
    for user in realm_users:
        user_wrappers.append(LdapUser.get_extended_user(user))
    return render(request,
                  'realm/realm_user.jinja2',
                  {
                      'realm': realm,
                      'realm_user': user_wrappers,
                      'success_headline': success_headline,
                      'success_text': success_text,
                  },
                  status=status_code,
                  )


def create_user(request, realm: Realm, form: AddLDAPUserForm):
    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    current_site = get_current_site(request)
    protocol = get_protocol(request=request)
    try:
        LdapUser.create_with_django_user_creation_and_welcome_mail(realm=realm,
                                                                   protocol=protocol,
                                                                   domain=current_site.domain,
                                                                   username=username,
                                                                   email=email)
        if realm.default_group:
            ldap_user = LdapUser.get_user(username=username, realm=realm)
            ldap_default_group = LdapGroup.get_group(group_name=realm.default_group.name, realm=realm)
            LdapGroup.add_user_to_groups(ldap_user=ldap_user, ldap_groups=[ldap_default_group, ])

        return get_realm_user_list(request=request,
                                   realm_id=realm.id,
                                   status_code=201,
                                   success_headline='Aktion erfolgreich',
                                   success_text=f'Nutzer {username} erfolgreich angelegt.',
                                   )
    except ALREADY_EXISTS:
        return render(request,
                      'user/realm_user_add.jinja2',
                      {
                          'form': form,
                          'realm': realm,
                          'extra_error': f'Nutzer {username} existiert bereits.',
                      },
                      status=409)


def get_protocol(request):
    return 'https' if request.is_secure() else 'http'
