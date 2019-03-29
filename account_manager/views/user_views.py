from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account_helper.models import Realm
from account_manager.forms import AddLDAPUserForm
from account_manager.models import LdapUser, LdapGroup
from account_manager.main_views import is_realm_admin


@login_required
@is_realm_admin
def realm_user(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm_obj.ldap_base_dn
    realm_users = LdapUser.objects.all()
    return render(request, 'realm/realm_user.jinja2', {'realm': realm_obj, 'realm_user': realm_users})


@login_required
@is_realm_admin
def user_detail(request, realm_id, user_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = realm.ldap_base_dn
    user = LdapUser.objects.get(dn=user_dn)
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
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
            LdapUser.objects.create(username=username,
                                    password=password, first_name=first_name,
                                    last_name=last_name, email=email)
            return redirect('realm-user-list', realm_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPUserForm()
    return render(request, 'user/user_add.jinja2', {'form': form, 'realm': realm_obj})


@login_required
@is_realm_admin
def user_update(request, realm_id, user_dn):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    if request.method == 'POST':
        form = AddLDAPUserForm(request.POST)
        if form.is_valid():
            ldap_user.username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if password:
                ldap_user.password = password
            ldap_user.first_name = form.cleaned_data['first_name']
            ldap_user.last_name = form.cleaned_data['last_name']
            ldap_user.email = form.cleaned_data['email']
            ldap_user.save()

            return redirect('realm-user-detail', realm_id, user_dn)
    else:
        form_data = {'username': ldap_user.username, 'first_name': ldap_user.first_name,
                     'last_name': ldap_user.last_name, 'email': ldap_user.email}
        form = AddLDAPUserForm(initial=form_data)
    return render(request, 'user/user_detail.jinja2', {'form': form, 'realm': realm_obj})


@login_required
@is_realm_admin
def user_delete(request, realm_id, user_dn):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
    LdapGroup.base_dn = f'ou=groups,{realm_obj.ldap_base_dn}'
    ldap_user = LdapUser.objects.get(dn=user_dn)
    user_groups = LdapGroup.objects.filter(members__contains=ldap_user.dn)
    for group in user_groups:
        group.members.remove(ldap_user.dn)
        group.save()
    ldap_user.delete()
    return redirect('realm-user-list', realm_id)