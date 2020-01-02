import logging
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPException
from socket import timeout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from ldap import LDAPError

from account_helper.models import Realm
from account_manager.utils.mail_utils import realm_send_mail
from account_manager.utils.main_views import render_permission_denied_view, render_realm_detail_view, \
    get_users_home_view
from .forms import RealmAddForm, RealmUpdateForm
from .models import LdapGroup, LdapUser

logger = logging.getLogger(__name__)


def is_realm_admin(view_func):
    def decorator(request, *args, **kwargs):
        realm_id = kwargs.get('realm_id', None)
        if realm_id and (request.user.is_superuser or len(
                Realm.objects.filter(id=realm_id).filter(
                    admin_group__user__username__contains=request.user.username)) > 0):
            return view_func(request, *args, **kwargs)
        else:
            return render_permission_denied_view(request)

    return decorator


@login_required
def realm_list(request):
    return get_users_home_view(request)


@login_required
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

                    realm = Realm.objects.create(name=name, ldap_base_dn=ldap_base_dn)
                    realm.save()
                    return render_realm_detail_view(request, realm.id, status_code=201)
                except IntegrityError as err:
                    # TODO: Load no extra fail view, use current add view
                    return render(request, 'realm/realm_add_failed.jinja2',
                                  {'realm_name': name, 'error': err}, status=409)
                except LDAPError as err:
                    logger.debug(f"Ldap Error: {err}")
                    return render(request, 'realm/realm_add_failed.jinja2',
                                  {'realm_name': name}, status=409)
        else:
            form = RealmAddForm()
        return render(request, 'realm/realm_add.jinja2', {'realms': realms, 'form': form})
    return render_permission_denied_view(request)


def base_dn_available(base_dn):
    LdapUser.base_dn = f'ou=people,{base_dn}'
    user = LdapUser.objects.create(username='dummy', first_name=' ', last_name=' ')
    user.delete()


@login_required
@is_realm_admin
def realm_detail(request, realm_id):
    return render_realm_detail_view(request, realm_id)


@login_required
@is_realm_admin
def realm_update(request, realm_id):
    if request.user.is_superuser:
        realm = Realm.objects.get(id=realm_id)

        LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
        ldap_admin_group = None if not realm.admin_group else LdapGroup.objects.get(name=realm.admin_group.name)
        ldap_default_group = None if not realm.default_group else LdapGroup.objects.get(name=realm.default_group.name)

        form_data = {'id': realm.id,
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
                realm.admin_group = None if not admin_ldap_group else admin_ldap_group.get_django_group()
                default_ldap_group = form.cleaned_data['default_group']
                realm.default_group = None if not default_ldap_group else default_ldap_group.get_django_group()
                realm.save()
                return render_realm_detail_view(request, realm_id, status_code=200)
            return render(request, 'realm/realm_update.jinja2', {'realm': realm, 'form': form}, status=422)
        else:
            form = RealmUpdateForm(initial=form_data)
        return render(request, 'realm/realm_update.jinja2', {'realm': realm, 'form': form})
    return render_permission_denied_view(request)


@login_required
@is_realm_admin
def realm_delete_confirm(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    return render(request, 'realm/realm_confirm_delete.jinja2', {'realm': realm})


@login_required
@is_realm_admin
def realm_delete(request, realm_id):
    if request.user.is_superuser:
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
        return get_users_home_view(request)
    return render_permission_denied_view(request)


def permission_denied(request):
    return render_permission_denied_view(request)


def realm_email_test(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    test_msg = f'Du hast die Mail Konfiguration für {realm.name} erfolgreich abgeschlossen.'
    success_msg = 'Test erfolgreich'
    error_msg_auth = f'Mail konnte nicht versendet werden, Anmeldedaten inkorrekt.'
    error_msg_connect = f'Mail konnte nicht versendet werden. Verbindungsaufbau abgelehnt. ' \
                        f'Bitte überprüfen sie die Server Addresse und den Port'
    error_msg_timeout = f'Mail konnte nicht versendet werden. Zeitüberschreitung beim Verbindungsaufbau. ' \
                        f'Bitte überprüfen sie die Server Addresse und den Port'
    error_msg_smtp = f'Mail konnte nicht versendet werden. Bitte kontaktieren sie den Administrator'
    try:
        realm_send_mail(realm, realm.email, f'{realm.name} Test Mail', test_msg)
    except SMTPAuthenticationError:
        return render_realm_detail_view(request, realm_id, error_headline="Testmail", error_text=error_msg_auth)
    except SMTPConnectError:
        return render_realm_detail_view(request, realm_id, error_headline="Testmail", error_text=error_msg_connect)
    except timeout:
        return render_realm_detail_view(request, realm_id, error_headline="Testmail", error_text=error_msg_timeout)
    except SMTPException:
        return render_realm_detail_view(request, realm_id, error_headline="Testmail", error_text=error_msg_smtp)
    return render_realm_detail_view(request, realm_id, success_headline="Testmail", success_text=success_msg)
