from django.shortcuts import render, redirect
from .models import LdapGroup, LdapUser
from .forms import AddLDAPUserForm, AddLDAPGroupForm, RealmAddForm, RealmUpdateForm
from account_helper.models import Realm
from django.contrib.auth.models import User, Group


# @login_required
# def userinfo(request):
#     try:
#         ldapuserprofile = UserProfile.objects.get(uid=request.user.username)
#     except UserProfile.DoesNotExist:
#         return HttpResponseRedirect('/login/')
#     context = {'request': request, 'ldapuser': ldapuserprofile, }
#     return render(request, 'myapp/userinfo.html', context)

def realm(request):
    realms = Realm.objects.all()
    if request.method == 'POST':
        form = RealmAddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ldap_rdn_org = form.cleaned_data['ldap_rdn_org']
            realm_obj = Realm.objects.create(name=name, ldap_rdn_org=ldap_rdn_org)
            realm_obj.save()
            return redirect('realm-detail', realm_obj.id)
    else:
        form = RealmAddForm()
    return render(request, 'realm/realm_home.jinja2', {'realms': realms, 'form': form})


def realm_detail(request, id):
    realm_obj = Realm.objects.get(id=id)
    return render(request, 'realm/realm_detailed.jinja2', {'realm': realm_obj})


def realm_update(request, id):
    if request.user.is_superuser:
        realm_obj = Realm.objects.get(id=id)
        data = {'id': realm_obj.id, 'ldap_base_dn': realm_obj.ldap_base_dn, 'name': realm_obj.name,
                'email': realm_obj.email,
                'admin_group': realm_obj.admin_group}
        if request.method == 'POST':
            form = RealmUpdateForm(request.POST)
            if form.is_valid():
                realm_obj.name = form.cleaned_data['name']
                realm_obj.ldap_base_dn = form.cleaned_data['ldap_base_dn']
                realm_obj.email = form.cleaned_data['email']

                admin_ldap_group = form.cleaned_data['admin_group']
                realm_obj.admin_group, _ = Group.objects.get_or_create(name=admin_ldap_group.name)
                realm_obj.save()
                return redirect('realm-detail', realm_obj.id)
        else:
            form = RealmUpdateForm(initial=data)
        return render(request, 'realm/realm_update.jinja2', {'realm': realm_obj, 'form': form})
    else:
        realm_obj = Realm.objects.get(id=id)
        return render(request, 'realm/realm_update.jinja2', {'realm': realm_obj})


def realm_user(request, id):
    realm_obj = Realm.objects.get(id=id)
    LdapUser.base_dn = realm_obj.ldap_base_dn
    realm_users = LdapUser.objects.all()
    return render(request, 'realm/realm_user.jinja2', {'realm': realm_obj, 'realm_user': realm_users})


def realm_groups(request, id):
    realm_obj = Realm.objects.get(id=id)
    LdapGroup.base_dn = realm_obj.ldap_base_dn
    realm_groups_obj = LdapGroup.objects.all()
    return render(request, 'realm/realm_groups.jinja2', {'realm': realm_obj, 'realm_groups': realm_groups_obj})


def userlist(request):
    LdapUser.base_dn = LdapUser.ROOT_DN
    LdapGroup.base_dn = LdapGroup.ROOT_DN
    user = LdapUser.objects.all()
    groups = LdapGroup.objects.all()
    context = {'users': user, 'groups': groups}

    return render(request, 'user/user_list.jinja2', context)


def user_detail(request, dn):
    user = LdapUser.objects.get(dn=dn)
    context = {'user': user, }
    return render(request, 'user/user_detail.jinja2', context)


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
            LdapUser.base_dn = realm_obj.ldap_base_dn
            LdapUser.objects.create(username=username,
                                    password=password, first_name=first_name,
                                    last_name=last_name, )
            return redirect('realm-user-list', realm_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPUserForm()
    return render(request, 'user/user_add.jinja2', {'form': form, 'realm': realm_obj})


def group_detail(request, dn):
    group = LdapGroup.objects.get(dn=dn)
    context = {'group': group, }
    return render(request, 'user/group_detail.jinja2', context)


def group_add(request, realm_id):
    realm_obj = Realm.objects.get(id=realm_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddLDAPGroupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            members = form.cleaned_data['members']
            members = [member.dn for member in members]
            LdapGroup.base_dn = realm_obj.ldap_base_dn
            LdapGroup.objects.create(name=name, members=members)
            return redirect('realm-group-list', realm_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPGroupForm()

    return render(request, 'group/group_add.jinja2', {'form': form, 'realm': realm_obj})
