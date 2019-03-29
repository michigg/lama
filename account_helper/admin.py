from django.contrib import admin
from .models import Realm, LdapGroupRDN, LdapUserRDN

# Register your models here.
admin.site.register(Realm)
admin.site.register(LdapGroupRDN)
admin.site.register(LdapUserRDN)
