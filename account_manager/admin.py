from django.contrib import admin
from .models import LdapGroup, LdapUser
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms


# Register your models here
class LdapUserAdmin(admin.ModelAdmin):
    exclude = ['dn', 'password', 'photo', 'phone', '']
    list_display = ['username', 'email']

    search_fields = ['first_name', 'last_name', 'full_name', 'username']


class LdapGroupForm(forms.ModelForm):
    usernames = forms.ModelMultipleChoiceField(
        queryset=LdapUser.objects.all(),
        widget=FilteredSelectMultiple('Users', is_stacked=False),
        required=False,
    )

    class Meta:
        exclude = []
        model = LdapGroup

    def clean_usernames(self):
        data = self.cleaned_data['usernames']
        if not data:
            return []

        return list(data.values_list('username', flat=True))


class LdapGroupAdmin(admin.ModelAdmin):
    form = LdapGroupForm
    exclude = ['dn', 'usernames', 'member']
    list_display = ['name']
    search_fields = ['name']


admin.site.register(LdapGroup, LdapGroupAdmin)
admin.site.register(LdapUser, LdapUserAdmin)
