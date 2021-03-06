import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from account_helper.models import Realm
from account_manager.forms import AddLDAPGroupForm
from account_manager.main_views import is_realm_admin
from account_manager.models import LdapGroup, LdapUser
from ldap import ALREADY_EXISTS


def protect_cross_realm_group_access(view_func):
    def decorator(request, *args, **kwargs):
        realm_id = kwargs.get('realm_id', None)
        group_dn = kwargs.get('group_dn', None)

        if realm_id and group_dn and Realm.objects.get(id=realm_id).ldap_base_dn not in group_dn:
            return render(request, 'permission_denied.jinja2',
                          {
                              'extra_errors':
                                  'Die angefragte Gruppe gehört einem anderen Bereich an. Gruppen können nur von dem Bereich bearbeitet werden, in dem sie erstellt wurden.'},
                          status=404)
        return view_func(request, *args, **kwargs)

    return decorator


@login_required
@is_realm_admin
def realm_groups(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = realm_obj.ldap_base_dn
    realm_groups_obj = LdapGroup.objects.all()
    return render(request, 'realm/realm_groups.jinja2', {'realm': realm_obj, 'realm_groups': realm_groups_obj})


@login_required
@is_realm_admin
@protect_cross_realm_group_access
def group_detail(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    group = LdapGroup.objects.get(dn=group_dn)
    users = LdapUser.get_users_by_dn(realm, group.members)
    user_wrapper = LdapUser.get_user_active_marked(users)
    return render(request, 'group/group_detail.jinja2', {'group': group, 'realm': realm, 'users': user_wrapper})


@login_required
@is_realm_admin
def group_add(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = LdapUser.ROOT_DN
    users = LdapUser.objects.all()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddLDAPGroupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            members = form.cleaned_data['members']
            members = [member.dn for member in members]
            LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
            try:
                LdapGroup.objects.create(name=name, description=description, members=members)
            except ALREADY_EXISTS:
                return render(request, 'group/group_add.jinja2', {'form': form, 'realm': realm, 'users': users,
                                                                  'extra_error': 'Der Gruppenname ist leider schon belegt. Bitte wähle einen anderen.'})
            return redirect('realm-group-list', realm_id)
        elif 'members' not in form.cleaned_data:
            return render(request, 'group/group_add.jinja2', {'form': form, 'realm': realm, 'users': users,
                                                              'extra_error': 'Bitte wähle mindestens ein Mitglied aus. Falls kein Mitglied angezeigt wird, erstelle zuerst einen Nutzer'})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPGroupForm()
    return render(request, 'group/group_add.jinja2', {'form': form, 'realm': realm, 'users': users})


@login_required
@is_realm_admin
@protect_cross_realm_group_access
def group_update(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = LdapUser.ROOT_DN
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'

    group = LdapGroup.objects.get(dn=group_dn)
    users = LdapUser.objects.all()
    if request.method == 'POST':
        form = AddLDAPGroupForm(request.POST)
        if form.is_valid():
            group.name = form.cleaned_data['name']
            group.description = form.cleaned_data['description']
            members = form.cleaned_data['members']
            group.members = [member.dn for member in members]
            group.save()
            return redirect('realm-group-detail', realm_id, group.dn)
        elif 'members' not in form.cleaned_data:
            return render(request, 'group/group_detail.jinja2',
                          {'form': form, 'realm': realm, 'group': group,
                           'extra_error': 'Gruppen dürfen nicht leer sein. Wenn du die Gruppe nicht mehr benutzen möchtest, solltest du Sie löschen'})
    else:
        members = LdapUser.objects.none()
        if group.members:
            members = LdapUser.get_users_by_dn(realm, group.members)
        data = {'name': group.name, 'description': group.description, 'members': members}
        form = AddLDAPGroupForm(initial=data)

    return render(request, 'group/group_detail.jinja2',
                  {'form': form, 'realm': realm, 'group': group, 'users': users})


@login_required
@is_realm_admin
@protect_cross_realm_group_access
def group_delete(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    group = LdapGroup.objects.get(dn=group_dn)
    if realm.admin_group and realm.admin_group.name == group.name:
        realm.admin_group = None
        realm.save()
    if realm.default_group and realm.default_group.name == group.name:
        realm.default_group = None
        realm.save()
    group.delete()

    return redirect('realm-group-list', realm_id)


@login_required
@is_realm_admin
@protect_cross_realm_group_access
def group_delete_confirm(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    group = LdapGroup.objects.get(dn=group_dn)
    return render(request, 'group/group_confirm_delete.jinja2',
                  {'realm': realm, 'group': group})
