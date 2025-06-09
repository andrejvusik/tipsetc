from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect

from blog.models import Comment, Post


@login_required
def post_add_comment(request, slug: str):
    if request.method != "POST":
        return HttpResponseBadRequest()

    post = get_object_or_404(Post, slug=slug)
    user = request.user
    content = request.POST.get("content")
    if not (content := content.strip()):
        return HttpResponseBadRequest()

    Comment.objects.create(content=content, user=user, post=post)

    context = {
        "comments": Comment.objects.filter(post=post).all(),
    }

    return render(request, "post/blocks/comments_list.html", context)

@login_required
def post_delete_comment(request, comment_id: int):
    if request.method != "POST":
        return HttpResponseBadRequest()

    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=comment.post.id)
    user = request.user
    if comment.user == user:
        comment.delete()

        context = {
            "comments": post.comments.all(),
        }

        return render (request, "post/blocks/comments_list.html", context)

    else:
        return HttpResponseBadRequest()

