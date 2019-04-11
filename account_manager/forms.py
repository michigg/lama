from django import forms

from .models import LdapUser, LdapGroup
from django.forms import modelformset_factory


class AddLDAPUserForm(forms.Form):
    username = forms.CharField(label='Nutzername', max_length=400)
    email = forms.EmailField(label='E-Mail')


class AdminUpdateLDAPUserForm(forms.Form):
    username = forms.CharField(label='Nutzername', max_length=400)
    email = forms.EmailField(label='E-Mail')
    password = forms.CharField(label='Passwort', widget=forms.PasswordInput, required=False)
    first_name = forms.CharField(label='Vorname', required=True)
    last_name = forms.CharField(label='Nachname', required=True)


class UpdateLDAPUserForm(forms.Form):
    email = forms.EmailField(label='E-Mail')
    first_name = forms.CharField(label='Vorname', required=True)
    last_name = forms.CharField(label='Nachname', required=True)
    # phone = forms.(db_column='telephoneNumber', blank=True)
    # mobile_phone = forms.CharField(db_column='mobile', blank=True)
    # photo = forms.ImageField(label='Profilfoto', required=False)


class UserDeleteListForm(forms.Form):
    ldap_users = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=LdapUser.objects.all())


class UserGroupListForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=LdapGroup.objects.all())


class AddLDAPGroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=400)
    # TODO show only allowed user
    members = forms.ModelMultipleChoiceField(label='Mitglieder', widget=forms.CheckboxSelectMultiple,
                                             queryset=LdapUser.objects.all(), )


class RealmAddForm(forms.Form):
    name = forms.CharField(label='Bereichsname', max_length=200)
    ldap_base_dn = forms.CharField(label='LDAP Base DN',
                                   help_text='TODO',
                                   max_length=200)


class RealmUpdateForm(forms.Form):
    ldap_base_dn = forms.CharField(label='LDAP Base DN',
                                   help_text='TODO',
                                   max_length=200)
    email = forms.EmailField(label='Bereichs E-Mail Adresse')
    name = forms.CharField(label='Bereichsname', max_length=200)
    admin_group = forms.ModelChoiceField(label='Admin Gruppe',
                                         help_text="Die Mitglieder dieser Gruppe darf den Bereich administieren",
                                         queryset=LdapGroup.objects.all(), required=False)
    default_group = forms.ModelChoiceField(label='Default Gruppe',
                                           help_text="Diese Gruppe wird jedem User der neu erstellt wird hinzugefügt werden",
                                           queryset=LdapGroup.objects.all(), required=False)


UserFormset = modelformset_factory(
    LdapUser,
    fields=('dn',),
    extra=1
)
