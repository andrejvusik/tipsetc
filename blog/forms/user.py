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

class UserBioForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']
