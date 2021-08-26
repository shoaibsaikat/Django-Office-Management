from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SigninForm

def signin(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        form = SigninForm(request.POST)
        if user is not None:
            login(request, user)
            return redirect('index')
    else:
        form = SigninForm()
    return render(request, 'accounts/signin.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('index')
