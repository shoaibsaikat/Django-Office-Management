from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from . import forms

def signin(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            form = forms.SigninForm()
    else:
        form = forms.SigninForm()

    return render(request, 'accounts/signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('index')
