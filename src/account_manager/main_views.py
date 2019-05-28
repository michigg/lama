import logging
import re
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPException
from socket import timeout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime, timedelta

from account_helper.models import Realm
from account_manager.utils.mail_utils import realm_send_mail
from .forms import RealmAddForm, RealmUpdateForm
from .models import LdapGroup, LdapUser
from ldap import LDAPError

logger = logging.getLogger(__name__)


def is_realm_admin(view_func):
    def decorator(request, *args, **kwargs):
        realm_id = kwargs.get('realm_id', None)
        if realm_id and (request.user.is_superuser or len(
                Realm.objects.filter(id=realm_id).filter(
                    admin_group__user__username__contains=request.user.username)) > 0):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('permission-denied')

    return decorator


@login_required
def realm_list(request):
    user = request.user
    if user.is_superuser:
        realms = Realm.objects.order_by('name').all()
    else:
        realms = Realm.objects.filter(admin_group__user__username__contains=user.username).order_by('name').order_by(
            'name')
    show_user = request.GET.get('show_user', False)
    if show_user or (len(realms) == 0 and not user.is_superuser):
        try:
            LdapUser.base_dn = LdapUser.ROOT_DN
            user = LdapUser.objects.get(username=user.username)
            realm_base_dn = re.compile('(uid=[a-zA-Z0-9_-]*),(ou=[a-zA-Z_-]*),(.*)').match(user.dn).group(3)
            realm = Realm.objects.get(ldap_base_dn=realm_base_dn)

            return redirect('user-detail', realm.id, user.dn)
        except ObjectDoesNotExist as err:
            logger.info('Anmeldung fehlgeschlagen', err)
            return HttpResponse("Invalid login. Please try again.")
    elif len(realms) == 1:
        return redirect('realm-detail', realms[0].id)
    else:
        realm_wrappers = []
        for realm in realms:
            realm_wrappers.append(_get_group_user_count_wrapper(realm))
        return render(request, 'realm/realm_home.jinja2', {'realms': realms, 'realm_wrappers': realm_wrappers})


def _get_group_user_count_wrapper(realm):
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    return {'realm': realm, 'group_count': LdapGroup.objects.count(), 'user_count': LdapUser.objects.count()}


@login_required
@is_realm_admin
def realm_add(request):
    if request.user.is_superuser:
        realms = Realm.objects.all().order_by('name')
        if request.method == 'POST':
            form = RealmAddForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                ldap_base_dn = form.cleaned_data['ldap_base_dn']
                try:
                    base_dn_available(ldap_base_dn)

                    realm_obj = Realm.objects.create(name=name, ldap_base_dn=ldap_base_dn)
                    realm_obj.save()
                    return redirect('realm-detail', realm_obj.id)
                except IntegrityError as err:
                    return render(request, 'realm/realm_add_failed.jinja2',
                                  {'realm_name': name, 'error': err})
                except LDAPError as err:
                    logger.debug("Ldap Error", err)
                    return render(request, 'realm/realm_add_failed.jinja2',
                                  {'realm_name': name})
        else:
            form = RealmAddForm()
        return render(request, 'realm/realm_add.jinja2', {'realms': realms, 'form': form})
    else:
        redirect('permission-denied')


def base_dn_available(base_dn):
    LdapUser.base_dn = f'ou=people,{base_dn}'
    user = LdapUser.objects.create(username='dummy', first_name=' ', last_name=' ')
    user.delete()


@login_required
@is_realm_admin
def realm_detail(request, realm_id):
    return render_realm_detail_page(realm_id, request)


def render_realm_detail_page(realm_id, request, notice=""):
    realm = Realm.objects.get(id=realm_id)
    ldap_admin_group, ldap_default_group = get_default_admin_group(realm)
    LdapUser.base_dn = realm.ldap_base_dn
    inactive_users = LdapUser.get_inactive_users().count()
    return render(request, 'realm/realm_detailed.jinja2',
                  {'realm': realm, 'ldap_admin_group': ldap_admin_group, 'ldap_default_group': ldap_default_group,
                   'inactive_user_count': inactive_users, 'users_count': LdapUser.objects.all().count(),
                   'notice': notice})


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


@login_required
@is_realm_admin
def realm_update(request, realm_id):
    if request.user.is_superuser:
        realm = Realm.objects.get(id=realm_id)
        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
        ldap_admin_group = None
        if realm.admin_group:
            ldap_admin_group = LdapGroup.objects.get(name=realm.admin_group.name)
        ldap_default_group = None
        if realm.default_group:
            ldap_default_group = LdapGroup.objects.get(name=realm.default_group.name)
        data = {'id': realm.id,
                'ldap_base_dn': realm.ldap_base_dn,
                'name': realm.name,
                'email': realm.email,
                'admin_group': ldap_admin_group,
                'default_group': ldap_default_group}
        if request.method == 'POST':
            form = RealmUpdateForm(request.POST)
            if form.is_valid():
                realm.name = form.cleaned_data['name']
                realm.ldap_base_dn = form.cleaned_data['ldap_base_dn']
                realm.email = form.cleaned_data['email']
                admin_ldap_group = form.cleaned_data['admin_group']
                if admin_ldap_group:
                    realm.admin_group, _ = Group.objects.get_or_create(name=admin_ldap_group.name)
                else:
                    realm.admin_group = None
                default_ldap_group = form.cleaned_data['default_group']
                if default_ldap_group:
                    realm.default_group, _ = Group.objects.get_or_create(name=default_ldap_group.name)
                else:
                    realm.default_group = None
                realm.save()
                return redirect('realm-detail', realm.id)
        else:
            form = RealmUpdateForm(initial=data)
        return render(request, 'realm/realm_update.jinja2', {'realm': realm, 'form': form})
    else:
        realm = Realm.objects.get(id=realm_id)
        return render(request, 'realm/realm_update.jinja2', {'realm': realm})


@login_required
@is_realm_admin
def realm_delete_confirm(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    return render(request, 'realm/realm_confirm_delete.jinja2', {'realm': realm})


@login_required
@is_realm_admin
def realm_delete(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm.ldap_base_dn
    LdapGroup.base_dn = realm.ldap_base_dn
    try:
        ldap_users = LdapUser.objects.all()
        ldap_usernames = [user.username for user in ldap_users]
        ldap_groups = LdapGroup.objects.all()
        ldap_groupnames = [group.name for group in ldap_groups]
        django_user = User.objects.filter(username__contains=ldap_usernames)
        django_groups = Group.objects.filter(name__contains=ldap_groupnames)
        for user in django_user:
            user.delete()
        for group in django_groups:
            group.delete()
        for user in ldap_users:
            user.delete()
        for group in ldap_groups:
            group.delete()
    except LDAPError:
        # TODO: Save delete
        pass
    realm.delete()
    return redirect('realm-home')


def permission_denied(request):
    return render(request, 'permission_denied.jinja2', {})


def realm_email_test(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    ldap_admin_group, ldap_default_group = get_default_admin_group(realm)
    try:
        realm_send_mail(realm, realm.email, f'{realm.name} Test Mail',
                        f'Du hast die Mail Konfiguration für {realm.name} erfolgreich abgeschlossen.')
    except SMTPAuthenticationError as err:
        return render(request, 'realm/realm_detailed.jinja2',
                      {'realm': realm, 'error': f'Mail konnte nicht versendet werden, Anmeldedaten inkorrekt.',
                       'ldap_admin_group': ldap_admin_group,
                       'ldap_default_group': ldap_default_group})
    except SMTPConnectError as err:
        return render(request, 'realm/realm_detailed.jinja2',
                      {'realm': realm,
                       'error': f'Mail konnte nicht versendet werden. Verbindungsaufbau abgelehnt. Bitte überprüfen sie die Server Addresse und den Port',
                       'ldap_admin_group': ldap_admin_group,
                       'ldap_default_group': ldap_default_group})
    except timeout as err:
        return render(request, 'realm/realm_detailed.jinja2',
                      {'realm': realm,
                       'error': f'Mail konnte nicht versendet werden. Zeitüberschreitung beim Verbindungsaufbau. Bitte überprüfen sie die Server Addresse und den Port',
                       'ldap_admin_group': ldap_admin_group,
                       'ldap_default_group': ldap_default_group})
    except SMTPException:
        return render(request, 'realm/realm_detailed.jinja2',
                      {'realm': realm,
                       'error': f'Mail konnte nicht versendet werden. Bitte kontaktieren sie den Administrator',
                       'ldap_admin_group': ldap_admin_group,
                       'ldap_default_group': ldap_default_group})
    return render_realm_detail_page(realm_id, request, notice='Test erfolgreich')
