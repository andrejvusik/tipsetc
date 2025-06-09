from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from blog.models import Post, PostLike, Comment, CommentLike


@login_required
def toggle_like(request, obj, object_id: int):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    if obj == "post":
        object_like = get_object_or_404(Post, id=object_id)
        like, created = PostLike.objects.get_or_create(user=request.user, post=object_like)

    elif obj == "comment":
        object_like = get_object_or_404(Comment, id=object_id)
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=object_like)

    if not created:
        like.delete()

    context = {
        "comment": object_like,
        "post": object_like,
    }

    return render(request, f'post/blocks/{obj}_like_button.html', context)