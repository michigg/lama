import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from account_helper.models import Realm
from account_manager.forms import AddLDAPGroupForm
from account_manager.main_views import is_realm_admin
from account_manager.models import LdapGroup, LdapUser


def protect_cross_realm_group_access(view_func):
    def decorator(request, *args, **kwargs):
        realm_id = kwargs.get('realm_id', None)
        group_dn = kwargs.get('group_dn', None)

        if realm_id and group_dn and Realm.objects.get(id=realm_id).ldap_base_dn not in group_dn:
            return HttpResponse("Ressource konnte nicht gefunden werden.", status=404)
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
    return render(request, 'group/group_detail.jinja2', {'group': group, 'realm': realm})


@login_required
@is_realm_admin
def group_add(request, realm_id):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = LdapUser.ROOT_DN
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddLDAPGroupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data["name"]
            members = form.cleaned_data['members']
            members = [member.dn for member in members]
            LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
            LdapGroup.objects.create(name=name, members=members)
            return redirect('realm-group-list', realm_id)
        elif 'members' not in form.cleaned_data:
            return render(request, 'group/group_add.jinja2', {'form': form, 'realm': realm,
                                                              'extra_error': 'Bitte wähle mindestens ein Mitglied aus. Falls kein Mitglied angezeigt wird, erstelle zuerst einen Nutzer'})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPGroupForm()
    return render(request, 'group/group_add.jinja2', {'form': form, 'realm': realm})


@login_required
@is_realm_admin
@protect_cross_realm_group_access
def group_update(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapUser.base_dn = LdapUser.ROOT_DN
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'

    group = LdapGroup.objects.get(dn=group_dn)

    if request.method == 'POST':
        form = AddLDAPGroupForm(request.POST)
        if form.is_valid():
            group.name = form.cleaned_data['name']
            members = form.cleaned_data['members']
            group.members = [member.dn for member in members]
            group.save()
            return redirect('realm-group-detail', realm_id, group.dn)
    else:
        members = LdapUser.objects.none()
        if group.members:
            group_members = [re.compile('uid=([a-zA-Z0-9_]*),(ou=[a-zA-Z_]*),(.*)').match(member).group(1) for
                             member in
                             group.members]
            query = Q(username=group_members.pop())
            for member in group_members:
                query = query | Q(username=member)
            members = LdapUser.objects.filter(query)
        data = {'name': group.name, 'members': members}
        form = AddLDAPGroupForm(initial=data)

    return render(request, 'group/group_detail.jinja2',
                  {'form': form, 'realm': realm, 'group': group})


@login_required
@is_realm_admin
@protect_cross_realm_group_access
def group_delete(request, realm_id, group_dn):
    realm = Realm.objects.get(id=realm_id)
    LdapGroup.base_dn = f'ou=groups,{realm.ldap_base_dn}'
    group = LdapGroup.objects.get(dn=group_dn)
    group.delete()

    return redirect('realm-group-list', realm_id)
