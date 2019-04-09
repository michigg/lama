from django import forms

from .models import LdapUser, LdapGroup


class AddLDAPUserForm(forms.Form):
    username = forms.CharField(label='Nutzername', max_length=400)
    email = forms.EmailField(label='E-Mail', required=False)


class UpdateLDAPUserForm(forms.Form):
    # username = forms.CharField(label='Nutzername', max_length=400)
    email = forms.EmailField(label='E-Mail')
    password = forms.CharField(label='Passwort', widget=forms.PasswordInput, required=False)
    first_name = forms.CharField(label='Vorname', required=True)
    last_name = forms.CharField(label='Nachname', required=True)
    # phone = forms.(db_column='telephoneNumber', blank=True)
    # mobile_phone = forms.CharField(db_column='mobile', blank=True)
    # photo = forms.ImageField(label='Profilfoto', required=False)


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
