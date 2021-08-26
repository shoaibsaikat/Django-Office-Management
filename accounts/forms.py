from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
