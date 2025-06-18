from django import forms

from blog.models import Post


class CreateEditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'published']
