from django.shortcuts import render, redirect
from .models import LdapGroup, LdapUser
from .forms import AddLDAPUserForm, AddLDAPGroupForm, RealmAddForm, RealmUpdateForm
from account_helper.models import Realm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required


def is_realm_admin(view_func):
    def decorator(request, *args, **kwargs):
        print(args)
        print(kwargs)
        realm_id = kwargs.get('id', None)
        if realm_id and (request.user.is_superuser or len(
                Realm.objects.filter(id=realm_id).filter(
                    admin_group__user__username__contains=request.user.username)) > 0):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('permission-denied')

    return decorator


@login_required
def realm_home(request):
    user = request.user
    if not user.is_superuser:
        realms = Realm.objects.filter(admin_group__user__username__contains=user.username)
        if len(realms) == 0:
            return redirect('user-detail')
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


@login_required
@is_realm_admin
def realm_detail(request, id):
    realm_obj = Realm.objects.get(id=id)
    return render(request, 'realm/realm_detailed.jinja2', {'realm': realm_obj})


@login_required
@is_realm_admin
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


@login_required
@is_realm_admin
def realm_user(request, id):
    realm_obj = Realm.objects.get(id=id)
    LdapUser.base_dn = realm_obj.ldap_base_dn
    realm_users = LdapUser.objects.all()
    return render(request, 'realm/realm_user.jinja2', {'realm': realm_obj, 'realm_user': realm_users})


@login_required
@is_realm_admin
def realm_groups(request, id):
    realm_obj = Realm.objects.get(id=id)
    LdapGroup.base_dn = realm_obj.ldap_base_dn
    realm_groups_obj = LdapGroup.objects.all()
    return render(request, 'realm/realm_groups.jinja2', {'realm': realm_obj, 'realm_groups': realm_groups_obj})


@login_required
def userlist(request):
    LdapUser.base_dn = LdapUser.ROOT_DN
    LdapGroup.base_dn = LdapGroup.ROOT_DN
    user = LdapUser.objects.all()
    groups = LdapGroup.objects.all()
    context = {'users': user, 'groups': groups}

    return render(request, 'user/user_list.jinja2', context)


@login_required
def user_detail(request, dn):
    user = LdapUser.objects.get(dn=dn)
    context = {'user': user, }
    return render(request, 'user/user_detail.jinja2', context)


@login_required
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
            LdapUser.base_dn = f'ou=people,{realm_obj.ldap_base_dn}'
            LdapUser.objects.create(username=username,
                                    password=password, first_name=first_name,
                                    last_name=last_name, )
            return redirect('realm-user-list', realm_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPUserForm()
    return render(request, 'user/user_add.jinja2', {'form': form, 'realm': realm_obj})


@login_required
def group_detail(request, dn):
    group = LdapGroup.objects.get(dn=dn)
    context = {'group': group, }
    return render(request, 'user/group_detail.jinja2', context)


@login_required
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
            LdapGroup.base_dn = f'ou=groups,{realm_obj.ldap_base_dn}'
            LdapGroup.objects.create(name=name, members=members)
            return redirect('realm-group-list', realm_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPGroupForm()

    return render(request, 'group/group_add.jinja2', {'form': form, 'realm': realm_obj})


def permission_denied(request):
    return render(request, 'permission_denied.jinja2', {})
