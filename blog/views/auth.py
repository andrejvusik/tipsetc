from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django import shortcuts
from django.conf import settings


User = get_user_model()


def user_signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Email not found. Please try again.')
        else:
            usr = User.objects.get(email=email)
            user = authenticate(request, username=usr.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back. Dear "{ user.username }", you have successfully logged in.')
                return shortcuts.redirect("posts")
            else:
                messages.error(request, 'Invalid password. Please try again.')
                return shortcuts.redirect("user_signin")

    context = {
        "settings": settings,
    }

    if not request.user.is_authenticated:
        return shortcuts.render(request, "auth/signin.html", context)
    return shortcuts.redirect("posts")


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
            messages.warning(request, f'Email "{email}" is already registered. Try using another email.')
        elif User.objects.filter(username=username).exists():
            messages.warning(request, f'Username "{username}" is already registered. Try using another username.')
        else:
            if password == password2:
                User.objects.create_user(username=username, email=email, password=password)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Dear "{user.username}", you have successfully registered.')
                    return shortcuts.redirect("posts")
                else:
                    return shortcuts.redirect("user_signin")
            else:
                messages.error(request, f'Passwords did not match. Please try again.')

    context = {
        "settings": settings,
    }

    if not request.user.is_authenticated:
        return shortcuts.render(request, "auth/signup.html", context)
    return shortcuts.redirect("posts")


def user_logout(request):
    messages.success(request, f'Dear "{ request.user }", you have successfully logged out.')
    logout(request)
    return shortcuts.redirect('posts')
