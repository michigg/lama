from django.shortcuts import render, redirect
from .models import LdapGroup, LdapUser
from .forms import AddLDAPUserForm, AddLDAPGroupForm


# @login_required
# def userinfo(request):
#     try:
#         ldapuserprofile = UserProfile.objects.get(uid=request.user.username)
#     except UserProfile.DoesNotExist:
#         return HttpResponseRedirect('/login/')
#     context = {'request': request, 'ldapuser': ldapuserprofile, }
#     return render(request, 'myapp/userinfo.html', context)


def userlist(request):
    user = LdapUser.objects.all()
    groups = LdapGroup.objects.all()
    context = {'users': user, 'groups': groups}
    # ldap_user = LdapUser.objects.get(username='fred')
    # ldap_user = LdapUser.objects.create(rdn='ou=people,ou=fs_wiai,ou=fachschaften', username='b3',
    #                                     password='lappen1', first_name='ferdinand1',
    #                                     last_name='red1', )
    # new_group = LdapGroup.objects.create(rdn='ou=groups,ou=fs_wiai,ou=fachschaften', name="funny_wiai12",
    #                                      members=['dc=stuve,dc=de'])
    # new_group.save()

    return render(request, 'user_list.jinja', context)


def user_detail(request, dn):
    user = LdapUser.objects.get(dn=dn)
    context = {'user': user, }
    return render(request, 'user_detail.jinja', context)


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
