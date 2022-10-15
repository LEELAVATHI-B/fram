from django.contrib import admin
from django.contrib.auth.admin import Group
from django_summernote.admin import SummernoteModelAdmin
from .models import Note, cubeUser, APIkey

# Register your models here.


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(cubeUser)
admin.site.unregister(Group)
admin.site.register(Note, PostAdmin)
admin.site.register(APIkey)
