from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from ldap import ALREADY_EXISTS, OBJECT_CLASS_VIOLATION
from account_helper.models import Realm
from account_manager.forms import AddLDAPUserForm, UserDeleteListForm, UpdateLDAPUserForm, AdminUpdateLDAPUserForm, \
    UserGroupListForm
from account_manager.main_views import is_realm_admin
from account_manager.models import LdapUser, LdapGroup


@login_required
@is_realm_admin
def realm_user(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm_obj.ldap_base_dn
    realm_users = LdapUser.objects.all()
    user_wrappers = []
    for user in realm_users:
        try:
            django_user = User.objects.get(username=user.username)
            if django_user.last_login:
                user_wrappers.append({'user': user, 'active': True})
            else:
                user_wrappers.append({'user': user, 'active': False})
        except ObjectDoesNotExist:
            user_wrappers.append({'user': user, 'active': False})
    return render(request, 'realm/realm_user.jinja2', {'realm': realm_obj, 'realm_user': user_wrappers})


@login_required
def realm_user_detail(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm.ldap_base_dn
    user = LdapUser.objects.get(dn=user_dn)
    LdapGroup.base_dn = LdapGroup.ROOT_DN
    groups = LdapGroup.objects.filter(members=user.dn)
    if realm_id and (request.user.is_superuser or len(
            Realm.objects.filter(id=realm_id).filter(
                admin_group__user__username__contains=request.user.username)) > 0):
        return render(request, 'user/realm_user_detail.jinja2', {'user': user, 'groups': groups, 'realm': realm})
    else:
        return render(request, 'user/user_detail.jinja2', {'user': user, 'groups': groups, 'realm': realm})


@login_required
@is_realm_admin
def user_add(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddLDAPUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            current_site = get_current_site(request)
            protocol = 'http'
            if request.is_secure():
                protocol = 'https'
            LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
            try:
                LdapUser.create_with_django_user_creation_and_welcome_mail(realm=realm,
                                                                           protocol=protocol,
                                                                           domain=current_site.domain,
                                                                           username=username,
                                                                           email=email)
                if realm.default_group:
                    user = LdapUser.objects.get(username=username)

                    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
                    default_ldap_group = LdapGroup.objects.get(name=realm.default_group.name)
                    ldap_add_user_to_groups(ldap_user=user.dn, user_groups=[default_ldap_group, ])

                return redirect('realm-user-list', realm_id)
            except ALREADY_EXISTS as err:
                return render(request, 'user/realm_user_add.jinja2', {'form': form, 'realm': realm,
                                                                      'extra_error': f'Nutzer {username} existiert bereits.'})
    else:
        form = AddLDAPUserForm()
    return render(request, 'user/realm_user_add.jinja2', {'form': form, 'realm': realm})


@login_required
@is_realm_admin
def realm_user_update(request, realm_id, user_dn):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    return user_update_controller(request=request,
                                  realm=realm_obj,
                                  ldap_user=ldap_user,
                                  redirect_name='realm-user-detail',
                                  update_view='user/realm_user_detail.jinja2',
                                  form_class=AdminUpdateLDAPUserForm,
                                  form_attrs=[
                                      {'model_field': 'username', 'form_field': 'username'},
                                      {'model_field': 'password', 'form_field': 'password'},
                                      {'model_field': 'first_name', 'form_field': 'first_name'},
                                      {'model_field': 'last_name', 'form_field': 'last_name'},
                                      {'model_field': 'email', 'form_field': 'email'}, ])


@login_required
@is_realm_admin
def realm_user_delete(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    if _is_deleteable_user(realm, ldap_user):
        user_delete_controller(ldap_user, realm)
        return redirect('realm-user-list', realm_id)
    else:
        return redirect('permission-denied')


@login_required
@is_realm_admin
def realm_user_delete_confirm(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    deletion_link = {'name': 'realm-user-delete', 'args': [realm.id, ldap_user.dn]}
    cancel_link = {'name': 'realm-user-detail', 'args': [realm.id, ldap_user.dn]}
    return render(request, 'user/user_confirm_delete.jinja2',
                  {'realm': realm, 'user': ldap_user, 'deletion_link': deletion_link, 'cancel_link': cancel_link})


@login_required
@is_realm_admin
def realm_multiple_user_delete(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    if request.method == 'POST':
        form = UserDeleteListForm(request.POST)
        if form.is_valid():
            ldap_users = form.cleaned_data['ldap_users']
            for ldap_user in ldap_users:
                if _is_deleteable_user(realm, ldap_user):
                    user_delete_controller(ldap_user, realm)
            return redirect('realm-user-list', realm_id)
    return redirect('realm-user-list', realm.id)


@login_required
@is_realm_admin
def realm_multiple_user_delete_confirm(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    if request.method == 'POST':
        form = UserDeleteListForm(request.POST)
        if form.is_valid():
            ldap_users = form.cleaned_data['ldap_users']
            deletable_users = []
            blocked_users = []
            for ldap_user in ldap_users:
                if _is_deleteable_user(realm, ldap_user):
                    deletable_users.append(ldap_user)
                else:
                    blocked_users.append(ldap_user)
            return render(request, 'realm/realm_user_multiple_delete.jinja2',
                          {'form': form, 'realm': realm, 'deletable_users': deletable_users,
                           'blocked_users': blocked_users,
                           'confirm': True})
    # TODO: Form not valid
    form = UserDeleteListForm()
    LdapUser.base_dn = realm.ldap_base_dn
    users = LdapUser.objects.all()
    return render(request, 'realm/realm_user_multiple_delete_confirm.jinja2',
                  {'form': form, 'realm': realm, 'users': users})


def _is_deleteable_user(realm, user):
    user_groups = LdapGroup.get_user_groups(realm, user, LdapGroup.ROOT_DN)
    user_group_names = [group.name for group in user_groups]
    user_admin_realms = Realm.objects.filter(id=realm.id).filter(admin_group__name__in=user_group_names)
    return not len(user_admin_realms) > 0


@login_required
def user_update(request, realm_id, user_dn):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    if request.user.username == ldap_user.username:
        return user_update_controller(request=request,
                                      realm=realm_obj,
                                      ldap_user=ldap_user,
                                      redirect_name='realm-user-detail',
                                      update_view='user/user_detail.jinja2',
                                      form_class=UpdateLDAPUserForm,
                                      form_attrs=[
                                          {'model_field': 'first_name', 'form_field': 'first_name'},
                                          {'model_field': 'last_name', 'form_field': 'last_name'},
                                          {'model_field': 'email', 'form_field': 'email'}, ])
    else:
        return redirect('permission-denied')


@login_required
def user_delete_confirm(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    if request.user.username == ldap_user.username:
        deletion_link = {'name': 'user-delete', 'args': [ldap_user.dn, realm.id]}
        cancel_link = {'name': 'realm-user-detail', 'args': [realm.id, ldap_user.dn]}
        return render(request, 'user/user_confirm_delete.jinja2',
                      {'realm': realm, 'user': ldap_user, 'deletion_link': deletion_link, 'cancel_link': cancel_link})
    else:
        return redirect('permission-denied')


@login_required
def user_delete(request, realm_id, user_dn):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    if request.user.username == ldap_user.username:
        user_delete_controller(ldap_user, realm_obj)
        return redirect('account-deleted', realm_id)
    else:
        return redirect('permission-denied')


@login_required
@is_realm_admin
def realm_user_group_update(request, realm_id, user_dn, error=None):
    realm = Realm.objects.get(id=realm_id)
    ldap_user, realm_groups_available, user_groups = get_available_given_groups(realm, user_dn)

    return render(request, 'user/realm_user_update_groups.jinja2',
                  {'realm': realm, 'user': ldap_user, 'user_groups': user_groups,
                   'realm_groups': realm_groups_available, 'extra_error': error})


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


@login_required
@is_realm_admin
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
                ldap_remove_user_from_groups(user_dn, groups)
            except OBJECT_CLASS_VIOLATION as err:
                ldap_user, realm_groups_available, user_groups = get_available_given_groups(realm, user_dn)
                return render(request, 'user/realm_user_update_groups.jinja2',
                              {'realm': realm, 'user': ldap_user, 'user_groups': user_groups,
                               'realm_groups': realm_groups_available,
                               'extra_error': 'Bearbeiten fehlgeschlagen. Der Nutzer scheint der letzte in einer Gruppe zu sein. Bitte löschen Sie die Gruppe zuerst.'})
    return redirect('realm-user-group-update', realm.id, user_dn)


def user_deleted(request, realm_id):
    return render(request, 'user/account_deleted.jinja2', {'realm': Realm.objects.get(id=realm_id)})


def user_update_controller(request, realm, ldap_user, redirect_name, update_view, form_class, form_attrs):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            for form_attr in form_attrs:
                if form.cleaned_data[form_attr['form_field']]:
                    ldap_user.__setattr__(form_attr['model_field'], form.cleaned_data[form_attr['form_field']])
                ldap_user.save()
            return redirect(redirect_name, realm.id, ldap_user.dn)
    else:
        form_data = {'username': ldap_user.username, 'first_name': ldap_user.first_name,
                     'last_name': ldap_user.last_name, 'email': ldap_user.email}
        form = form_class(initial=form_data)
    return render(request, update_view, {'form': form, 'realm': realm, 'user': ldap_user})


def user_delete_controller(ldap_user, realm):
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    user_groups = LdapGroup.objects.filter(members__contains=ldap_user.dn)
    ldap_remove_user_from_groups(ldap_user.dn, user_groups)
    ldap_user.delete()
    try:
        django_user = User.objects.get(username=ldap_user.username)
        django_user.delete()
    except ObjectDoesNotExist:
        pass
    return


def ldap_remove_user_from_groups(ldap_user, user_groups):
    for group in user_groups:
        group.members.remove(ldap_user)
        group.save()


def ldap_add_user_to_groups(ldap_user, user_groups):
    for group in user_groups:
        group.members.append(ldap_user)
        group.save()


class LdapPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data['new_password1']
        LdapUser.base_dn = LdapUser.ROOT_DN
        LdapUser.password_reset(user, password)
        return super().form_valid(form)


class LdapPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data['new_password1']
        LdapUser.base_dn = LdapUser.ROOT_DN
        LdapUser.password_reset(user, password)
        return super().form_valid(form)
