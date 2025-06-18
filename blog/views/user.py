from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django import shortcuts
from django.shortcuts import get_object_or_404

from blog.forms import UserBioForm, UserEmailForm, UserNamesForm
from blog.models import UserProfile

User = get_user_model()


def user_profile(request, user_id):
    if not User.objects.filter(id=user_id).exists():
        messages.error(request, 'User not found. Please try again.')
        return shortcuts.redirect('posts')
    else:
        user = User.objects.get(id=user_id)
        context = {
            "settings": settings,
            'user_profile': UserProfile.objects.get(user=user),
        }
        return shortcuts.render(request, 'user/user_profile.html', context)


def user_bio_update(request):
    if not User.objects.filter(id=request.user.id).exists():
        messages.error(request, 'User not found. Please try again.')
        return shortcuts.redirect('posts')
    else:
        updated_user_profile = UserProfile.objects.get(user=request.user)
        form = UserBioForm(request.POST or None, UserProfile)
        if request.method == 'POST':
            if form.is_valid():
                bio = form.cleaned_data["bio"]
                updated_user_profile.bio = bio

                updated_user_profile.save()

                context = {
                    "user_profile": updated_user_profile,
                    "form": form,
                }

                return shortcuts.render(request, 'user/blocks/user_profile_bio.html', context)

        context = {
            "user_profile": updated_user_profile,
            "form": form,
        }
        return shortcuts.render(request, 'user/blocks/user_profile_bio.html', context)


def user_email_update(request):
    if not User.objects.filter(id=request.user.id).exists():
        messages.error(request, 'User not found. Please try again.')
        return shortcuts.redirect('posts')
    else:
        user = get_object_or_404(User, id=request.user.id)
        updated_user_profile = get_object_or_404(UserProfile, user=user)
        form = UserEmailForm(request.POST or None, User)
        if request.method == 'POST':
            if form.is_valid():
                email = request.POST.get('email')

                if user.email != email and User.objects.filter(email=email).exists():
                    # messages.warning(request, f'Email "{email}" is already registered. Try using another email.')
                    return shortcuts.redirect('user_email_update')
                else:
                    user.email = email
                    user.save()

                    context = {
                        "user_profile": updated_user_profile,
                        "form": form,
                    }

                    return shortcuts.render(
                        request,
                        'user/blocks/user_profile_email.html',
                        context
                    )

        context = {
            "user_profile": updated_user_profile,
            "form": form,
        }
        return shortcuts.render(request, 'user/blocks/user_profile_email.html', context)

def user_names_update(request):
    if not User.objects.filter(id=request.user.id).exists():
        messages.error(request, 'User not found. Please try again.')
        return shortcuts.redirect('posts')
    else:
        user = User.objects.get(id=request.user.id)
        form = UserNamesForm(request.POST or None, User)
        if request.method == 'POST':
            if form.is_valid():
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('username')

                user.first_name = first_name
                user.last_name = last_name

                user.save()

                if user.username != username and User.objects.filter(username=username).exists():
                    messages.warning(request, f'Username "{username}" is already registered. Try using another username.')
                    return shortcuts.redirect('user_names_update')
                else:
                    user.username = username
                    user.save()
                    updated_user_profile = get_object_or_404(UserProfile, user=user)

                    context = {
                        "user_profile": updated_user_profile,
                        "form": form,
                    }

                    return shortcuts.render(
                        request,
                        'user/blocks/user_profile_names.html',
                        context
                    )

        updated_user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            "user_profile": updated_user_profile,
            "form": form,
        }
        return shortcuts.render(request, 'user/blocks/user_profile_names.html', context)
