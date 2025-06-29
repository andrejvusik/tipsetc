from django import forms
from django.contrib.auth import get_user_model

from blog.models import UserProfile


User = get_user_model()

class UserNamesForm(forms.Form):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class UserEmailForm(forms.Form):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserPasswordForm(forms.Form):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),

        }

class UserBioForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']
