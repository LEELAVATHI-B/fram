from django.contrib import admin
from django.contrib.auth.admin import Group

# Register your models here.
from . models import cubeUser

admin.site.register(cubeUser)
admin.site.unregister(Group)

