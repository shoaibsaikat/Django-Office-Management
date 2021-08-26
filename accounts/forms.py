from django import forms
from django.contrib.auth.models import User

class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']