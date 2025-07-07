from django.http.response import HttpResponseBadRequest

from blog.models import Post, PostRating

from django import shortcuts
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def rate_post(request, post_id):
    post = shortcuts.get_object_or_404(Post, id=post_id)
    post_rating, created = PostRating.objects.get_or_create(user=request.user, post=post)
    if post_rating is None:
        return HttpResponseBadRequest(f"You have not rated post: \"{post.title}\".")

    if request.method == "POST":
        rating = int(request.POST.get("rate"))
        post_rating.rating = rating
        post_rating.save()
        # messages.success(request, f"You rated post: \"{post.title}\" on {rating} .")

    context = {
        "post": post,
        "users_rating": post_rating.rating,
    }

    return shortcuts.render(request, "post/blocks/post_rate.html", context)
