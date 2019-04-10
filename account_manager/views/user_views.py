from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from account_helper.models import Realm
from account_manager.forms import AddLDAPUserForm, UserDeleteListForm, UpdateLDAPUserForm, AdminUpdateLDAPUserForm
from account_manager.main_views import is_realm_admin
from account_manager.models import LdapUser, LdapGroup


@login_required
@is_realm_admin
def realm_user(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm_obj.ldap_base_dn
    realm_users = LdapUser.objects.all()
    return render(request, 'realm/realm_user.jinja2', {'realm': realm_obj, 'realm_user': realm_users})


@login_required
def realm_user_detail(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm.ldap_base_dn
    user = LdapUser.objects.get(dn=user_dn)
    groups = LdapGroup.objects.filter(members=user.dn)
    if realm_id and (request.user.is_superuser or len(
            Realm.objects.filter(id=realm_id).filter(
                admin_group__user__username__contains=request.user.username)) > 0):
        return render(request, 'user/realm_user_detail.jinja2', {'user': user, 'realm': realm})
    else:
        return render(request, 'user/user_detail.jinja2', {'user': user, 'groups': groups, 'realm': realm})


@login_required
@is_realm_admin
def user_add(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
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
            LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
            LdapUser.create_with_django_user_creation_and_welcome_mail(realm=realm_obj,
                                                                       protocol=protocol,
                                                                       domain=current_site.domain,
                                                                       username=username,
                                                                       email=email)
            return redirect('realm-user-list', realm_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPUserForm()
    return render(request, 'user/realm_user_add.jinja2', {'form': form, 'realm': realm_obj})


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
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    user_delete_controller(ldap_user, realm_obj)
    return redirect('realm-user-list', realm_id)


def realm_multiple_user_delete(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    if request.method == 'POST':
        form = UserDeleteListForm(request.POST)
        if form.is_valid():
            ldap_users = form.cleaned_data['ldap_users']
            for ldap_user in ldap_users:
                # TODO: Failure catchup
                user_delete_controller(ldap_user, realm)
            return redirect('realm-user-list', realm_id)
    # TODO: Form not valid
    form = UserDeleteListForm()
    LdapUser.base_dn = realm.ldap_base_dn
    users = LdapUser.objects.all()
    return render(request, 'realm/realm_user_multiple_delete.jinja2', {'form': form, 'realm': realm, 'users': users})


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
                                          {'model_field': 'password', 'form_field': 'password'},
                                          {'model_field': 'first_name', 'form_field': 'first_name'},
                                          {'model_field': 'last_name', 'form_field': 'last_name'},
                                          {'model_field': 'email', 'form_field': 'email'}, ])
    else:
        return redirect('permission-denied')


# # ldap_user.username = form.cleaned_data['username']

@login_required
def user_delete_confirm(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    if request.user.username == ldap_user.username:
        return render(request, 'user/user_confirm_delete.jinja2', {'realm': realm, 'user': ldap_user})
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
    print(user_groups)
    for group in user_groups:
        print(group)
        # LdapGroup.base_dn = group.base_dn
        group.members.remove(ldap_user.dn)
        group.save()
    ldap_user.delete()
    try:
        django_user = User.objects.get(username=ldap_user.username)
        django_user.delete()
    except ObjectDoesNotExist:
        pass
    return


class LdapPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        user = form.save()
        password = form.cleaned_data['new_password1']
        LdapUser.password_reset(user, password)
        return super().form_valid(form)
