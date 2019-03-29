from django.shortcuts import render, redirect
from .models import LdapGroup, LdapUser
from .forms import AddLDAPUserForm, AddLDAPGroupForm, RealmAddForm, RealmUpdateForm
from account_helper.models import Realm


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
    return render(request, 'realm/realm_home.jinja', {'realms': realms, 'form': form})


def realm_detail(request, id):
    if request.user.is_superuser:
        realm_obj = Realm.objects.get(id=id)
        data = {'id': realm_obj.id, 'ldap_rdn_org': realm_obj.ldap_rdn_org, 'name': realm_obj.name,
                'email': realm_obj.email,
                'admin_group': realm_obj.admin_group}
        if request.method == 'POST':
            form = RealmUpdateForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                ldap_rdn_org = form.cleaned_data['ldap_rdn_org']
                realm_obj = Realm.objects.create(name=name, ldap_rdn_org=ldap_rdn_org)
                realm_obj.save()
                return redirect('realm-detail', realm_obj.id)
        else:
            form = RealmUpdateForm(initial=data)
            return render(request, 'realm/realm_detailed.jinja', {'realm': realm_obj, 'form': form})
    else:
        realm_obj = Realm.objects.get(id=id)
        return render(request, 'realm/realm_detailed.jinja', {'realm': realm_obj})


def userlist(request):
    user = LdapUser.objects.all()
    groups = LdapGroup.objects.all()
    context = {'users': user, 'groups': groups}

    return render(request, 'user_list.jinja', context)


def user_detail(request, dn):
    user = LdapUser.objects.get(dn=dn)
    context = {'user': user, }
    return render(request, 'user_detail.jinja', context)


def group_detail(request, dn):
    group = LdapGroup.objects.get(dn=dn)
    context = {'group': group, }
    return render(request, 'group_detail.jinja', context)


def adduser(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddLDAPUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            rdn = form.cleaned_data['rdn']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            LdapUser.objects.create(rdn=rdn, username=username,
                                    password=password, first_name=first_name,
                                    last_name=last_name, )
            return redirect('user-list')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPUserForm()

    return render(request, 'user_add.jinja', {'form': form})


def addgroup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddLDAPGroupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            rdn = form.cleaned_data['rdn']
            name = form.cleaned_data['name']
            members = form.cleaned_data['members']
            members = [member.dn for member in members]
            LdapGroup.objects.create(rdn=rdn, name=name, members=members)
            return redirect('user-list')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddLDAPGroupForm()

    return render(request, 'group_add.jinja', {'form': form})
