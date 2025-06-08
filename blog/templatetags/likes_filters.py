from blog.models import Comment, Post

from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def comment_is_liked_by(comment: Comment, user: User) -> bool:
    return comment.is_liked_by(user)

@register.filter
def post_is_liked_by(post: Post, user: User) -> bool:
    return post.is_liked_by(user)
