from django import forms
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget

from .models import Note


class Noteform(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=SummernoteWidget())


class ProfilePicUpdate(forms.Form):
    profile_pic = forms.ImageField()
