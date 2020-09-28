from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login
from .forms import SignUpForm
from django.contrib.auth.models import User


def home(request):
    return render(request, 'authenticate/home.html')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('authenticate:home')
        else:
            form = SignUpForm(request.POST)
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'authenticate/register.html', context)






