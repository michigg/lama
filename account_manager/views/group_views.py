from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account_helper.models import Realm
from account_manager.forms import AddLDAPGroupForm
from account_manager.models import LdapGroup, LdapUser
from account_manager.main_views import is_realm_admin


@login_required
@is_realm_admin
def realm_groups(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = realm_obj.ldap_base_dn
    realm_groups_obj = LdapGroup.objects.all()
    return render(request, 'realm/realm_groups.jinja2', {'realm': realm_obj, 'realm_groups': realm_groups_obj})


@login_required
@is_realm_admin
def group_detail(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    group = LdapGroup.objects.get(dn=group_dn)
    return render(request, 'group/group_detail.jinja2', {'group': group, 'realm': realm})


@login_required
@is_realm_admin
def group_add(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = LdapUser.ROOT_DN
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddLDAPGroupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            members = form.cleaned_data['members']
            members = [member.dn for member in members]
            LdapGroup.base_dn = f'ou=groups,{realm_obj.ldap_base_dn}'
            LdapGroup.objects.create(name=name, members=members)
            return redirect('realm-group-list', realm_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPGroupForm()

    return render(request, 'group/group_add.jinja2', {'form': form, 'realm': realm_obj})


@login_required
@is_realm_admin
def group_update(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    group = LdapGroup.objects.get(dn=group_dn)
    LdapUser.base_dn = LdapUser.ROOT_DN
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddLDAPGroupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            group.name = form.cleaned_data['name']
            members = form.cleaned_data['members']
            group.members = [member.dn for member in members]
            group.save()
            return redirect('realm-group-detail', realm_id, group.dn)

    # if a GET (or any other method) we'll create a blank form
    else:
        # TODO: Automatic checkbox selection
        data = {'name': group.name, 'members': group.members}
        form = AddLDAPGroupForm(initial=data)

    return render(request, 'group/group_detail.jinja2', {'form': form, 'realm': realm})


def group_delete(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    group = LdapGroup.objects.get(dn=group_dn)
    group.delete()

    return redirect('realm-group-list', realm_id)
