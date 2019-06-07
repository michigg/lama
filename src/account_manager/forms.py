from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

from account_manager.utils.django_user import update_dajngo_user
from .models import LdapUser, LdapGroup
from django.forms import modelformset_factory
import logging

logger = logging.getLogger(__name__)


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
    phone = forms.CharField(label='Festnetz', required=False)
    mobile_phone = forms.CharField(label='Mobiltelefon', required=False)
    # photo = forms.ImageField(label='Profilfoto', required=False)


class UserDeleteListForm(forms.Form):
    ldap_users = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=LdapUser.objects.all())


class UserGroupListForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=LdapGroup.objects.all())


class AddLDAPGroupForm(forms.Form):
    name = forms.CharField(label='Gruppenname', max_length=400)
    description = forms.CharField(label='Beschreibung', max_length=1024, required=False)
    members = forms.ModelMultipleChoiceField(label='Nutzer hinzufügen', widget=forms.CheckboxSelectMultiple,
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

UserModel = get_user_model()


class LdapPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
             This allows subclasses to more easily customize the default policies
             that prevent inactive users and users with unusable passwords from
             resetting their password.
             """
        LdapUser.base_dn = LdapUser.ROOT_DN
        ldap_users = LdapUser.objects.filter(email=email)
        for ldap_user in ldap_users:
            update_dajngo_user(ldap_user)
        logger.debug('Pasword reset get users')
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        logger.debug((u for u in active_users))
        return (u for u in active_users)
