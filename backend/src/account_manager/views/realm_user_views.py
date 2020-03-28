from _ldap import OBJECT_CLASS_VIOLATION
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.shortcuts import render, redirect

from account_helper.models import Realm, DeletedUser
from account_manager.forms import AddLDAPUserForm, AdminUpdateLDAPUserForm, UserDeleteListForm, UserGroupListForm
from account_manager.main_views import is_realm_admin
from account_manager.models import LdapUser, LdapGroup
from account_manager.utils.django_user import update_dajngo_user
from account_manager.utils.mail_utils import send_welcome_mail
from account_manager.utils.user_views import get_realm_user_list, render_realm_user_detail_view, create_user, \
    user_update_controller, get_protocol, _is_deleteable_user, user_delete_controller, get_deletable_blocked_users, \
    get_available_given_groups, ldap_add_user_to_groups
from account_manager.views.user_views import protect_cross_realm_user_access, logger, multiple_user_delete_controller


@login_required
@is_realm_admin
def realm_user_list(request, realm_id):
    return get_realm_user_list(request, realm_id)


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_detail(request, realm_id, user_dn):
    return render_realm_user_detail_view(request, realm_id, user_dn)


@login_required
@is_realm_admin
def realm_user_add(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = AddLDAPUserForm(request.POST)
        if form.is_valid():
            return create_user(request, realm, form)
    else:
        form = AddLDAPUserForm()
    return render(request, 'user/realm_user_add.jinja2', {'form': form, 'realm': realm})


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_update(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
    return user_update_controller(request=request,
                                  realm=realm,
                                  ldap_user=ldap_user,
                                  user_detail_render_method=render_realm_user_detail_view,
                                  update_view='user/realm_user_detail.jinja2',
                                  form_class=AdminUpdateLDAPUserForm,
                                  form_attrs=[
                                      {'model_field': 'username', 'form_field': 'username'},
                                      {'model_field': 'first_name', 'form_field': 'first_name'},
                                      {'model_field': 'last_name', 'form_field': 'last_name'},
                                      {'model_field': 'email', 'form_field': 'email'}, ])


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_resend_password_reset(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
    try:
        if ldap_user.email:
            logger.info(f"Sending email to {ldap_user.email}")
            form = PasswordResetForm({'email': ldap_user.email})
            if form.is_valid():
                logger.info('CREATE REQUEST')
                pw_reset_request = HttpRequest()
                pw_reset_request.META['SERVER_NAME'] = get_current_site(request).domain
                pw_reset_request.META['SERVER_PORT'] = '80'
                if request.is_secure():
                    pw_reset_request.META['SERVER_PORT'] = '443'
                logger.info('form.save')
                form.save(
                    request=pw_reset_request,
                    use_https=True,
                    from_email=realm.email,
                    email_template_name='registration/password_reset_email.html')
                return render_realm_user_detail_view(request,
                                                     realm_id,
                                                     user_dn,
                                                     success_headline="Erfolgreich",
                                                     success_text="Die Passwort zurücksetzen E-Mail wurde erfolgreich versendet.")
            return render_realm_user_detail_view(request,
                                                 realm_id,
                                                 user_dn,
                                                 error_headline="Fehlgeschlagen",
                                                 error_text="Der Nutzer E-Mail Addresse ist ungültig. "
                                                            "Es wurde keine E-Mail übermittelt."
                                                 )
        return render_realm_user_detail_view(request,
                                             realm_id,
                                             user_dn,
                                             error_headline="Fehlgeschlagen",
                                             error_text="Der Nutzer besitzt keine E-Mail Addresse. "
                                                        "Bitte tragen Sie diese nach und probieren es erneut."
                                             )
    except Exception as err:
        logger.error(f'Error: {err}')
        return render_realm_user_detail_view(request,
                                             realm_id,
                                             user_dn,
                                             error_headline="Fehlgeschlagen",
                                             error_text="Die Passwort zurücksetzen E-Mail konnte nicht versendet werden.")


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_resend_welcome_mail(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)

    update_dajngo_user(ldap_user)
    current_site = get_current_site(request)
    protocol = get_protocol(request)
    send_welcome_mail(domain=current_site.domain,
                      email=ldap_user.email,
                      protocol=protocol,
                      realm=realm,
                      user=User.objects.get(username=ldap_user.username))
    return render_realm_user_detail_view(request,
                                         realm_id,
                                         user_dn,
                                         success_headline="Willkommensmail",
                                         success_text="Willkommensmail erfolgreich versendet.")


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_delete(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    if _is_deleteable_user(realm, ldap_user):
        try:
            return user_delete_controller(request=request, ldap_user=ldap_user, realm=realm)
        except OBJECT_CLASS_VIOLATION:
            deletion_link = {'name': 'realm-user-delete', 'args': [realm.id, ldap_user.dn]}
            cancel_link = {'name': 'realm-user-detail', 'args': [realm.id, ldap_user.dn]}
            return render(request, 'user/user_confirm_delete.jinja2',
                          {'realm': realm, 'user': ldap_user, 'deletion_link': deletion_link,
                           'cancel_link': cancel_link,
                           'extra_errors': f'Der Nutzer {ldap_user.username} konnte nicht gelöscht werden, '
                                           f'da er der letzte Nutzer einer Gruppe ist. '
                                           f'Bitte lösche die Gruppe zuerst oder trage einen anderen Nutzer '
                                           f'in die Gruppe ein.',
                           })

    else:
        return render(request, 'permission_denied.jinja2', {
            'extra_errors': f'Der Nutzer, {ldap_user.username}, gehört anscheinend zu den Admins. '
                            f'Solange der Nutzer dieser Gruppe angehört kann dieser nicht gelöscht werden. '
                            f'Bitte trage vorher den Nutzer aus der Admin Gruppe aus.'
        }, )


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_direct_delete(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
    if _is_deleteable_user(realm, ldap_user):
        username = ldap_user.username
        ldap_user.delete_complete()
        return get_realm_user_list(request=request, realm_id=realm_id, success_headline="Löschen erfolgreich",
                                   success_text=f"Nutzer {username} wurde erfolgreich gelöscht.")
    else:
        return render(request, 'permission_denied.jinja2', {
            'extra_errors': f'Der Nutzer, {ldap_user.username}, gehört anscheinend zu den Admins. '
                            f'Solange der Nutzer dieser Gruppe angehört kann dieser nicht gelöscht werden. '
                            f'Bitte trage vorher den Nutzer aus der Admin Gruppe aus.'
        }, )


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_delete_confirm(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
    deletion_link = {'name': 'realm-user-delete', 'args': [realm.id, ldap_user.dn]}
    cancel_link = {'name': 'realm-user-detail', 'args': [realm.id, ldap_user.dn]}
    return render(request, 'user/user_confirm_delete.jinja2',
                  {
                      'realm': realm,
                      'user': ldap_user,
                      'deletion_link': deletion_link,
                      'cancel_link': cancel_link,
                      'deletion_wait_days': settings.DELETION_WAIT_DAYS
                  })


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_delete_cancel(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    ldap_user = LdapUser.get_user_by_dn(dn=user_dn, realm=realm)
    try:
        deleted_user = DeletedUser.objects.get(ldap_dn=ldap_user.dn)
        deleted_user.delete()
    except ObjectDoesNotExist:
        return render_realm_user_detail_view(request=request, realm_id=realm_id, user_dn=user_dn,
                                             error_headline="Fehlgeschlagen",
                                             error_text="Nutzer ist nicht als gelöscht markiert.", status_code=409)

    return render_realm_user_detail_view(request=request, realm_id=realm_id, user_dn=user_dn,
                                         success_headline="Erfolgreich",
                                         success_text="Nutzerlöschung wurde abgebrochen")


@login_required
@is_realm_admin
def realm_multiple_user_delete(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    if request.method == 'POST':
        form = UserDeleteListForm(request.POST)
        if form.is_valid():
            return multiple_user_delete_controller(request, form, realm)
    return redirect('realm-user-list', realm.id)


@login_required
@is_realm_admin
def realm_multiple_user_delete_inactive(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    if request.method == 'POST':
        form = UserDeleteListForm(request.POST)
        if form.is_valid():
            ldap_users = form.cleaned_data['ldap_users']
            blocked_users, deletable_users = get_deletable_blocked_users(ldap_users, realm)
            return render(request, 'realm/realm_user_multiple_delete.jinja2',
                          {'form': form, 'realm': realm, 'deletable_users': deletable_users,
                           'blocked_users': blocked_users,
                           'confirm': True})
    inactive_users = LdapUser.get_inactive_users(realm=realm)

    # TODO: Form not valid
    form = UserDeleteListForm()
    return render(request, 'realm/realm_user_multiple_delete_confirm.jinja2',
                  {'form': form, 'realm': realm, 'users': inactive_users, })


@login_required
@is_realm_admin
def realm_multiple_user_delete_confirm(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    if request.method == 'POST':
        form = UserDeleteListForm(request.POST)
        if form.is_valid():
            ldap_users = form.cleaned_data['ldap_users']
            blocked_users, deletable_users = get_deletable_blocked_users(ldap_users, realm)
            return render(request, 'realm/realm_user_multiple_delete.jinja2',
                          {'form': form, 'realm': realm, 'deletable_users': deletable_users,
                           'blocked_users': blocked_users,
                           'confirm': True})
    # TODO: Form not valid
    form = UserDeleteListForm()
    users = LdapUser.get_users(realm=realm)
    return render(request, 'realm/realm_user_multiple_delete_confirm.jinja2',
                  {'form': form, 'realm': realm, 'users': users})


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_group_update(request, realm_id, user_dn, error=None):
    realm = Realm.objects.get(id=realm_id)
    ldap_user, realm_groups_available, user_groups = get_available_given_groups(realm, user_dn)

    return render(request, 'user/realm_user_update_groups.jinja2',
                  {'realm': realm, 'user': ldap_user, 'user_groups': user_groups,
                   'realm_groups': realm_groups_available, 'extra_error': error})


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_group_update_add(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'

    if request.method == 'POST':
        form = UserGroupListForm(request.POST)
        if form.is_valid():
            group_names = form.cleaned_data['groups']
            groups = []
            for group_name in group_names:
                groups.append(LdapGroup.objects.get(name=group_name))
            ldap_add_user_to_groups(user_dn, groups)
    return redirect('realm-user-group-update', realm.id, user_dn)


@login_required
@is_realm_admin
@protect_cross_realm_user_access
def realm_user_group_update_delete(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'

    if request.method == 'POST':
        form = UserGroupListForm(request.POST)
        if form.is_valid():
            group_names = form.cleaned_data['groups']
            groups = []
            for group_name in group_names:
                groups.append(LdapGroup.objects.get(name=group_name))
            try:
                LdapGroup.remove_user_from_groups(user_dn, groups)
            except OBJECT_CLASS_VIOLATION as err:
                ldap_user, realm_groups_available, user_groups = get_available_given_groups(realm, user_dn)
                return render(request, 'user/realm_user_update_groups.jinja2',
                              {'realm': realm, 'user': ldap_user, 'user_groups': user_groups,
                               'realm_groups': realm_groups_available,
                               'extra_error': 'Bearbeiten fehlgeschlagen. Der Nutzer scheint der letzte in einer Gruppe zu sein. Bitte löschen Sie die Gruppe zuerst.'})
    return redirect('realm-user-group-update', realm.id, user_dn)
