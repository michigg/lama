from django import forms

from .models import LdapUser, LdapGroup


class AddLDAPUserForm(forms.Form):
    username = forms.CharField(label='Nutzername', max_length=400)
    email = forms.EmailField(label='E-Mail', required=False)


class UserDeleteListForm(forms.Form):
    ldap_users = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=LdapUser.objects.all())


class AddLDAPGroupForm(forms.Form):
    name = forms.CharField(label='name', max_length=400)
    # TODO show only allowed user
    members = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=LdapUser.objects.all())


class RealmAddForm(forms.Form):
    name = forms.CharField(label='Bereichsname', max_length=200)
    ldap_base_dn = forms.CharField(label='LDAP Base DN',
                                   help_text='TODO',
                                   max_length=200)


class RealmUpdateForm(forms.Form):
    ldap_base_dn = forms.CharField(label='LDAP Base DN',
                                   help_text='TODO',
                                   max_length=200)
    name = forms.CharField(label='Bereichsname', max_length=200)
    admin_group = forms.ModelChoiceField(label='Admin Grouppe',
                                         help_text="Die Mitglieder dieser Gruppe darf den Bereich administieren",
                                         queryset=LdapGroup.objects.all())


class EmailSettingsForm(forms.Form):
    email = forms.EmailField(label='Eigene E-Mail Adresse')
