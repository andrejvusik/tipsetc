from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django import shortcuts
from django.shortcuts import get_object_or_404

from blog.forms import UserBioForm, UserEmailForm, UserNamesForm, UserPasswordForm
from blog.models import UserProfile, Subscription

User = get_user_model()


def user_profile(request, user_id):
    if not User.objects.filter(id=user_id).exists():
        messages.error(request, 'User not found. Please try again.')
        return shortcuts.redirect('posts')
    else:
        user = User.objects.get(id=user_id)
        is_subscribed = Subscription.objects.filter(subscriber=request.user.profile, subscribed_to=user.profile).exists()
        context = {
            "settings": settings,
            'user_profile': UserProfile.objects.get(user=user),
            'user_posts': user.posts.all(),
            'user_posts_for_all': user.posts.filter(published="for_all"),
            'user_posts_for_subscribers': user.posts.filter(published="for_subscribers"),
            'user_posts_draft': user.posts.filter(published="draft"),
            'is_subscribed': is_subscribed,
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

def user_password_update(request):
    if not User.objects.filter(id=request.user.id).exists():
        messages.error(request, 'User not found. Please try again.')
        return shortcuts.redirect('posts')
    else:
        user = User.objects.get(id=request.user.id)
        form = UserPasswordForm(request.POST or None, User)
        if request.method == 'POST':
            if form.is_valid():
                old_password = request.POST.get('old_password')
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                usr = authenticate(request, username=user.username, password=old_password)
                if not usr:
                    messages.error(request, 'Your old password was entered incorrectly. Please try again.')
                    return shortcuts.redirect('user_profile', user_id=user.id)
                elif new_password1 != new_password2:
                    messages.error(request, 'Your new passwords do not match.')
                    return shortcuts.redirect('user_profile', user_id = user.id)
                else:
                    user.set_password(new_password1)
                    user.save()
                    login(request, user)
                    messages.success(request, 'Your password was successfully updated.')
                    return shortcuts.redirect('user_profile', user_id = user.id)
        return None

def user_sub_unsub_scribe(request, user_id):
    if not User.objects.filter(id=user_id).exists():
        messages.error(request, 'User not found. Please try again.')
        return shortcuts.redirect('posts')
    else:
        subscribed_to = UserProfile.objects.get(user=User.objects.get(id=user_id))

        if Subscription.objects.filter(subscriber=request.user.profile, subscribed_to=subscribed_to).exists():
            Subscription.objects.filter(subscriber=request.user.profile, subscribed_to=subscribed_to).delete()
        else:
            Subscription.objects.create(subscriber=request.user.profile, subscribed_to=subscribed_to)
    return shortcuts.redirect('user_profile', user_id = user_id)
