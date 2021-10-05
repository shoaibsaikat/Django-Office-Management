from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import fields

from .models import Profile

class SigninForm(forms.ModelForm):
    username = forms.CharField(
        help_text="Enter your username",
        required=True,)
    password = forms.CharField(
        help_text="Enter your password",
        required=True,
        widget=forms.PasswordInput(),)
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def clean(self):
        cd = self.cleaned_data
        user = authenticate(username=cd.get('username'), password=cd.get('password'))
        if user is None:
            raise forms.ValidationError("wrong username or password")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('supervisor',)
        labels = {
            'supervisor': '',
        }

class InfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
