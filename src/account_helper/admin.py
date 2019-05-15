from django.contrib import admin
from .models import Realm, DeletedUser

# Register your models here.
admin.site.register(Realm)
admin.site.register(DeletedUser)
