from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings

from . import posts


def user_signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        usr =  User.objects.get(email=email)
        username = usr.username
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back. Dear "{ user.username }", you have successfully logged in.')
            return redirect("posts")
        else:
            return redirect("user_signin")

    context = {
        "settings": settings,
    }

    if not request.user.is_authenticated:
        return render(request, "auth/signin.html", context)
    return posts(request)

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        usr = User.objects.get(email=email)

        if usr is not None:
            messages.warning(request, f'Email "{email}" is already registered. Try using another email.')
        else:
            if password == password2:
                User.objects.create_user(username=username, email=email, password=password)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Dear "{user.username}", you have successfully registered.')
                    return redirect("posts")
                else:
                    return redirect("user_signin")

    context = {
        "settings": settings,
    }

    if not request.user.is_authenticated:
        return render(request, "auth/signup.html", context)
    return posts(request)

def user_logout(request):
    messages.success(request, f'Dear "{ request.user }", you have successfully logged out.')
    logout(request)
    return redirect('posts')
