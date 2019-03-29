from django import forms
from django.contrib.auth.models import User, Group
from account_helper.models import LdapUserRDN, LdapGroupRDN
from .models import LdapUser, LdapGroup


class AddLDAPUserForm(forms.Form):
    rdn = forms.ModelChoiceField(queryset=LdapUserRDN.objects.all())
    username = forms.CharField(label='Nutzername', max_length=400)
    first_name = forms.CharField(label='Vorname', max_length=400)
    last_name = forms.CharField(label='Nachname', max_length=400)
    password = forms.CharField(widget=forms.PasswordInput)


class AddLDAPGroupForm(forms.Form):
    rdn = forms.ModelChoiceField(queryset=LdapGroupRDN.objects.all())
    name = forms.CharField(label='name', max_length=400)
    members = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=LdapUser.objects.all())


class RealmAddForm(forms.Form):
    name = forms.CharField(label='Bereichsname', max_length=200)
    ldap_rdn_org = forms.CharField(label='LDAP OU Pfad',
                                   help_text='Angabe des Pfads zur Organisation, die die Ordnungseinheiten people und groups enthält. Ohne Routdn. Besipiel: "ou=people, ou=fs_wiai, ou=fachschaften, dc=stuve, dc=de" => ou=fs_wiai, ou=fachschaften, dc=stuve',
                                   max_length=200)


class RealmUpdateForm(forms.Form):
    ldap_rdn_org = forms.CharField(label='LDAP OU Pfad',
                                   help_text='Angabe des Pfads zur Organisation, die die Ordnungseinheiten people und groups enthält. Ohne Routdn. Besipiel: "ou=people, ou=fs_wiai, ou=fachschaften, dc=stuve, dc=de" => ou=fs_wiai, ou=fachschaften, dc=stuve',
                                   max_length=200)
    name = forms.CharField(label='Bereichsname', max_length=200)
    email = forms.EmailField(label='E-Mail', required=False)
    admin_group = forms.ModelChoiceField(label='Admin Grouppe',
                                         help_text="Die Mitglieder dieser Gruppe darf den Bereich administieren",
                                         queryset=LdapGroup.objects.all())
