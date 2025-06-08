from contextlib import redirect_stderr

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
def post_delete_comment(request, id: int):
    comment = get_object_or_404(Comment, id=id)
    post = get_object_or_404(Post, id=comment.post.id)
    user = request.user
    if comment.user == user:
        comment.delete()
        messages.success(request, f'{comment.user} your comment to  the post "{comment.post}" deleted successfully.')

        return redirect("post_view", slug=post.slug)

    else:
        return HttpResponseBadRequest()

