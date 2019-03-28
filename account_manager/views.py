from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import LdapGroup, LdapUser
from django.contrib.auth.models import User


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
    context = {'users': user, }
    # ldap_user = LdapUser.objects.get(username='fred')
    # ldap_user = LdapUser.objects.create(rdn='ou=people,ou=fs_sowi,ou=fachschaften', username='a123456789',
    #                                     password='lappen1', first_name='ferdinand1',
    #                                     last_name='red1', )
    # new_group = LdapGroup.objects.create(rdn='ou=groups,ou=fs_sowi,ou=fachschaften', name="funny_sowi1",
    # members = ['dc=stuve,dc=de'])
    # new_group.save()

    return render(request, 'user_list.jinja', context)


def changelist(request, dn):
    user = User.objects.get(id=uid)
    context = {'user': user, }
    return render(request, 'user_detail.jinja', context)
