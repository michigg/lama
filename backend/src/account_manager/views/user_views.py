import logging
from urllib.parse import urlencode

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from ldap import OBJECT_CLASS_VIOLATION

from account_helper.models import Realm
from account_manager.forms import UpdateLDAPUserForm, LdapPasswordChangeForm
from account_manager.models import LdapUser, LdapGroup
from account_manager.utils.user_views import render_user_detail_view, user_update_controller, user_delete_controller, \
    get_deletable_blocked_users, _is_deleteable_user

logger = logging.getLogger(__name__)


def protect_cross_realm_user_access(view_func):
    def decorator(request, *args, **kwargs):
        realm_id = kwargs.get('realm_id', None)
        user_dn = kwargs.get('user_dn', None)

        if realm_id and user_dn and Realm.objects.get(id=realm_id).ldap_base_dn not in user_dn:
            return render(request, 'permission_denied.jinja2',
                          {
                              'extra_errors': _(
                                  'Der angefragte Nutzer gehört einem anderen Bereich an. '
                                  'Nutzer können nur von dem Bereich bearbeitet werden, in dem sie erstellt wurden.'),
                          },
                          status=404)
        return view_func(request, *args, **kwargs)

    return decorator


@login_required
def user_detail(request, realm_id, user_dn):
    return render_user_detail_view(request, realm_id, user_dn)


def multiple_user_delete_controller(request, form, realm):
    ldap_users = form.cleaned_data['ldap_users']
    for ldap_user in ldap_users:
        if _is_deleteable_user(realm, ldap_user):
            try:
                user_delete_controller(request=request, ldap_user=ldap_user, realm=realm)
            except OBJECT_CLASS_VIOLATION:
                blocked_users, deletable_users = get_deletable_blocked_users(ldap_users, realm)
                return render(request,
                              'realm/realm_user_multiple_delete.jinja2',
                              {
                                  'form': form,
                                  'realm': realm,
                                  'deletable_users': deletable_users,
                                  'blocked_users': blocked_users,
                                  'confirm': True,
                                  'extra_errors': f'Nutzer {ldap_user} konnte nicht gelöscht werden, '
                                                  f'da er der letzte Nutzer einer Gruppe ist. '
                                                  f'Bitte tragen Sie vorher den Nutzer aus der Gruppe aus. '
                                                  f'Das löschen der restlichen Nutzer wurde unterbrochen.',
                              }, )
    return redirect('realm-user-list', realm.id)


@login_required
def user_update(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
    if request.user.username == ldap_user.username:
        return user_update_controller(request=request,
                                      realm=realm,
                                      ldap_user=ldap_user,
                                      user_detail_render_method=render_user_detail_view,
                                      update_view='user/user_detail.jinja2',
                                      form_class=UpdateLDAPUserForm,
                                      form_attrs=[
                                          {'model_field': 'first_name', 'form_field': 'first_name'},
                                          {'model_field': 'last_name', 'form_field': 'last_name'},
                                          {'model_field': 'email', 'form_field': 'email'},
                                          {'model_field': 'phone', 'form_field': 'phone'},
                                          {'model_field': 'mobile_phone', 'form_field': 'mobile_phone'}, ])
    return redirect('permission-denied')


@login_required
def user_delete_confirm(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
    if request.user.username == ldap_user.username:
        deletion_link = {'name': 'user-delete', 'args': [realm.id, ldap_user.dn]}
        cancel_link = {'name': 'user-detail', 'args': [realm.id, ldap_user.dn]}
        return render(request, 'user/user_confirm_delete.jinja2',
                      {'realm': realm, 'user': ldap_user, 'deletion_link': deletion_link, 'cancel_link': cancel_link})
    else:
        return redirect('permission-denied')


@login_required
def user_delete(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)

    if request.user.username == ldap_user.username:
        user_delete_controller(request=request, ldap_user=ldap_user, realm=realm)
        return redirect('account-deleted', realm_id)
    else:
        return redirect('permission-denied')


@login_required
def password_change_controller(request):
    logout(request)
    base_url = reverse('login')
    next_param = reverse('password_change')
    query_string = urlencode({'next': next_param})
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)


class LdapPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data['new_password1']
        LdapUser.base_dn = LdapUser.ROOT_DN
        LdapUser.password_reset(user, password)
        cached_redirect = super().form_valid(form)
        user.set_unusable_password()
        user.save()
        return cached_redirect


class LdapPasswordChangeView(PasswordChangeView):
    form_class = LdapPasswordChangeForm

    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data['new_password1']
        LdapUser.base_dn = LdapUser.ROOT_DN
        LdapUser.password_reset(user, password)
        cached_request = super().form_valid(form)
        user.set_unusable_password()
        user.save()
        return cached_request
