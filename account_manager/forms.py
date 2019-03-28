from django import forms
from rdn_helper.models import LdapUserRDN, LdapGroupRDN
from .models import LdapUser


class AddLDAPUserForm(forms.Form):
    rdn = forms.ModelChoiceField(queryset=LdapUserRDN.objects.all())
    username = forms.CharField(label='username', max_length=400)
    first_name = forms.CharField(label='first_name', max_length=400)
    last_name = forms.CharField(label='last_name', max_length=400)
    password = forms.CharField(widget=forms.PasswordInput)


class AddLDAPGroupForm(forms.Form):
    rdn = forms.ModelChoiceField(queryset=LdapGroupRDN.objects.all())
    name = forms.CharField(label='name', max_length=400)
    members = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=LdapUser.objects.all())
