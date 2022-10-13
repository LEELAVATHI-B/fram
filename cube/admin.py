from django.contrib import admin
from django.contrib.auth.admin import Group
from django_summernote.admin import SummernoteModelAdmin
from .models import Note

# Register your models here.
from .models import cubeUser


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(cubeUser)
admin.site.unregister(Group)
admin.site.register(Note, PostAdmin)
