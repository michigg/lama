from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from account_helper.models import Realm
from account_manager.forms import AddLDAPUserForm, UserDeleteListForm, UpdateLDAPUserForm
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
    if realm_id and (request.user.is_superuser or len(
            Realm.objects.filter(id=realm_id).filter(
                admin_group__user__username__contains=request.user.username)) > 0):
        return render(request, 'user/realm_user_detail.jinja2', {'user': user, 'realm': realm})
    else:
        return render(request, 'user/user_detail.jinja2', {'user': user, 'realm': realm})


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
    return user_update_controller(ldap_user, realm_id, realm_obj, request, user_dn, 'realm-user-detail',
                                  'user/realm_user_detail.jinja2')


@login_required
@is_realm_admin
def realm_user_delete(request, realm_id, user_dn):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    user_delete_controller(ldap_user)
    return redirect('realm-user-list', realm_id)


def realm_multiple_user_delete(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    if request.method == 'POST':
        form = UserDeleteListForm(request.POST)
        if form.is_valid():
            ldap_users = form.cleaned_data['ldap_users']
            for ldap_user in ldap_users:
                # TODO: Failure catchup
                user_delete_controller(ldap_user)
            return redirect('realm-user-list', realm_id)
    # TODO: Form not valid
    form = UserDeleteListForm()
    return render(request, 'realm/realm_user_multiple_delete.jinja2', {'form': form, 'realm': realm})


@login_required
def user_update(request, realm_id, user_dn):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    if request.user.username == ldap_user.username:
        return user_update_controller(ldap_user, realm_id, realm_obj, request, user_dn, 'realm-user-detail',
                                      'user/user_detail.jinja2')
    else:
        return redirect('permission-denied')


@login_required
def user_delete(request, realm_id, user_dn):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    if request.user.username == ldap_user.username:
        user_delete_controller(ldap_user)
        return redirect('account-deleted', realm_id)
    else:
        return redirect('permission-denied')


def user_deleted(request, realm_id):
    return render(request, 'account_deleted.jinja2', {'realm': Realm.objects.get(id=realm_id)})


def user_update_controller(ldap_user, realm_id, realm_obj, request, user_dn, redirect_name, detail_page):
    if request.method == 'POST':
        form = UpdateLDAPUserForm(request.POST)
        if form.is_valid():
            # ldap_user.username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if password:
                ldap_user.password = password
            ldap_user.first_name = form.cleaned_data['first_name']
            ldap_user.last_name = form.cleaned_data['last_name']
            ldap_user.email = form.cleaned_data['email']
            ldap_user.save()

            return redirect(redirect_name, realm_id, user_dn)
    else:
        form_data = {'username': ldap_user.username, 'first_name': ldap_user.first_name,
                     'last_name': ldap_user.last_name, 'email': ldap_user.email}
        form = UpdateLDAPUserForm(initial=form_data)
    return render(request, detail_page, {'form': form, 'realm': realm_obj})


def user_delete_controller(ldap_user):
    user_groups = LdapGroup.objects.filter(members__contains=ldap_user.dn)

    for group in user_groups:
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
