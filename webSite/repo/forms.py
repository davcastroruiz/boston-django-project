from django.contrib.auth.models import User
from django import forms
from models import Url


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        exclude = ('site',)
        fields = ['url_title', 'url']