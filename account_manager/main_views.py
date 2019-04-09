import re
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPException
from socket import timeout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect

from account_helper.models import Realm
from account_manager.utils.mail_utils import realm_send_mail
from .forms import RealmAddForm, RealmUpdateForm, EmailSettingsForm
from .models import LdapGroup, LdapUser


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
    if not user.is_superuser:
        realms = Realm.objects.filter(admin_group__user__username__contains=user.username)
        if len(realms) == 0:
            user = LdapUser.objects.get(username=user.username)
            realm_base_dn = re.compile('(uid=[a-zA-Z0-9_]*),(ou=[a-zA-Z_]*),(.*)').match(user.dn).group(3)
            realm = Realm.objects.get(ldap_base_dn=realm_base_dn)
            return redirect('realm-user-detail', realm.id, user.dn)
        elif len(realms) == 1:
            return redirect('realm-detail', realms[0].id)
        else:
            return render(request, 'realm/realm_home.jinja2', {'realms': realms})
    else:
        realms = Realm.objects.all()
        if request.method == 'POST':
            form = RealmAddForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                ldap_base_dn = form.cleaned_data['ldap_base_dn']
                realm_obj = Realm.objects.create(name=name, ldap_base_dn=ldap_base_dn)
                realm_obj.save()
                return redirect('realm-detail', realm_obj.id)
        else:
            form = RealmAddForm()
        return render(request, 'realm/realm_home.jinja2', {'realms': realms, 'form': form})


@login_required
@is_realm_admin
def realm_detail(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
    return render(request, 'realm/realm_detailed.jinja2', {'realm': realm_obj})


@login_required
@is_realm_admin
def realm_update(request, realm_id):
    if request.user.is_superuser:
        realm_obj = Realm.objects.get(id=realm_id)
        data = {'id': realm_obj.id, 'ldap_base_dn': realm_obj.ldap_base_dn, 'name': realm_obj.name,
                'admin_group': realm_obj.admin_group}
        if request.method == 'POST':
            form = RealmUpdateForm(request.POST)
            if form.is_valid():
                realm_obj.name = form.cleaned_data['name']
                realm_obj.ldap_base_dn = form.cleaned_data['ldap_base_dn']
                admin_ldap_group = form.cleaned_data['admin_group']
                realm_obj.admin_group, _ = Group.objects.get_or_create(name=admin_ldap_group.name)
                realm_obj.save()
                return redirect('realm-detail', realm_obj.id)
        else:
            form = RealmUpdateForm(initial=data)
        return render(request, 'realm/realm_update.jinja2', {'realm': realm_obj, 'form': form})
    else:
        realm_obj = Realm.objects.get(id=realm_id)
        return render(request, 'realm/realm_update.jinja2', {'realm': realm_obj})


def realm_delete(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm.ldap_base_dn
    LdapGroup.base_dn = realm.ldap_base_dn
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
    realm.delete()
    return redirect('realm-home')


def permission_denied(request):
    return render(request, 'permission_denied.jinja2', {})


@login_required
@is_realm_admin
def realm_email_update(request, realm_id):
    realm = Realm.objects.get(id=realm_id)

    if request.method == 'POST':
        form = EmailSettingsForm(request.POST)
        if form.is_valid():
            realm.email = form.cleaned_data['email']
            realm.save()
            return redirect('realm-detail', realm.id)
    else:
        data = {}
        if realm.email:
            data = {'email': realm.email, }
        form = EmailSettingsForm(initial=data)
    return render(request, 'realm/realm_create_update_mail.jinja2', {'realm': realm, 'form': form})


def realm_email_test(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    try:
        realm_send_mail(realm, realm.email, f'{realm.name} Test Mail',
                        f'Du hast die Mail Konfiguration für {realm.name} erfolgreich abgeschlossen.')
    except SMTPAuthenticationError as err:
        return render(request, 'realm/realm_detailed.jinja2',
                      {'realm': realm, 'error': f'Mail konnte nicht versendet werden, Anmeldedaten inkorrekt.'})
    except SMTPConnectError as err:
        return render(request, 'realm/realm_detailed.jinja2',
                      {'realm': realm,
                       'error': f'Mail konnte nicht versendet werden. Verbindungsaufbau abgelehnt. Bitte überprüfen sie die Server Addresse und den Port'})
    except timeout as err:
        return render(request, 'realm/realm_detailed.jinja2',
                      {'realm': realm,
                       'error': f'Mail konnte nicht versendet werden. Zeitüberschreitung beim Verbindungsaufbau. Bitte überprüfen sie die Server Addresse und den Port'})
    except SMTPException:
        return render(request, 'realm/realm_detailed.jinja2',
                      {'realm': realm,
                       'error': f'Mail konnte nicht versendet werden. Bitte kontaktieren sie den Administrator'})
    return render(request, 'realm/realm_detailed.jinja2', {'realm': realm, 'notice': 'Test erfolgreich'})