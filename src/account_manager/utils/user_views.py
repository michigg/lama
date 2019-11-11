import logging

from _ldap import ALREADY_EXISTS
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render

from account_helper.models import Realm, DeletedUser
from account_manager.forms import AddLDAPUserForm
from account_manager.models import LdapUser, LdapGroup
from account_manager.utils.mail_utils import send_deletion_mail

logger = logging.getLogger(__name__)


def render_user_detail_view(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn)
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


def render_realm_user_detail_view(request, realm_id, user_dn, success_headline=None, success_text=None):
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


def user_update_controller(request, realm, ldap_user, user_detail_render_method, update_view, form_class,
                           form_attrs):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            for form_attr in form_attrs:
                # if form.cleaned_data[form_attr['form_field']]:
                logger.info(form.cleaned_data[form_attr['form_field']])
                ldap_user.__setattr__(form_attr['model_field'], form.cleaned_data[form_attr['form_field']])
            ldap_user.display_name = f'{form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}'
            logger.debug(form.data)
            ldap_user.save()
            return user_detail_render_method(request, realm.id, ldap_user.dn)
    else:
        form_data = {'username': ldap_user.username, 'first_name': ldap_user.first_name,
                     'last_name': ldap_user.last_name, 'email': ldap_user.email, 'phone': ldap_user.phone,
                     'mobile_phone': ldap_user.mobile_phone}
        form = form_class(initial=form_data)
    return render(request, update_view, {'form': form, 'realm': realm, 'user': ldap_user})


def user_deleted(request, realm_id):
    return render(request, 'user/account_deleted.jinja2', {'realm': Realm.objects.get(id=realm_id)})


def user_delete_controller(ldap_user, realm):
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    try:
        django_user = User.objects.get(username=ldap_user.username)
        try:
            DeletedUser.objects.create(user=django_user, ldap_dn=ldap_user.dn)
            send_deletion_mail(realm=realm, user=ldap_user)
        except IntegrityError as err:
            pass

    except ObjectDoesNotExist:
        pass
    return


def ldap_add_user_to_groups(ldap_user, user_groups):
    for group in user_groups:
        group.members.append(ldap_user)
        group.save()


def get_available_given_groups(realm, user_dn):
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    user_groups = LdapGroup.objects.filter(members=ldap_user.dn)
    realm_groups = LdapGroup.objects.all()
    realm_groups_available = []
    for realm_group in realm_groups:
        if realm_group not in user_groups:
            realm_groups_available.append(realm_group)
    return ldap_user, realm_groups_available, user_groups


def get_deletable_blocked_users(ldap_users, realm):
    deletable_users = []
    blocked_users = []
    for ldap_user in ldap_users:
        if _is_deleteable_user(realm, ldap_user):
            deletable_users.append(ldap_user)
        else:
            blocked_users.append(ldap_user)
    return blocked_users, deletable_users


def _is_deleteable_user(realm, user):
    user_groups = LdapGroup.get_user_groups(realm, user)
    user_group_names = [group.name for group in user_groups]
    user_admin_realms = Realm.objects.filter(id=realm.id).filter(admin_group__name__in=user_group_names)
    return not len(user_admin_realms) > 0
