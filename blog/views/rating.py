from django.http.response import HttpResponseBadRequest

from blog.models import Post, PostRating

from django import shortcuts
from django.contrib.auth.decorators import login_required

from blog.tasks.posts import update_post_rating_again, update_post_rating_new


@login_required
def rate_post(request, post_id):
    post = shortcuts.get_object_or_404(Post, id=post_id)
    if not PostRating.objects.filter(post=post, user=request.user).exists():
        users_rating = 0
    else:
        post_rating = PostRating.objects.filter(post=post, user=request.user).first()
        users_rating = old_rating = post_rating.rating


    # post_rating, created = PostRating.objects.get_or_create(user=request.user, post=post)
    # if post_rating is None:
    #     return HttpResponseBadRequest(f"You have not rated post: \"{post.title}\".")

    if request.method == "POST":
        rating = int(request.POST.get("rate"))

        if not PostRating.objects.filter(post=post, user=request.user).exists():
            post_rating, created = PostRating.objects.get_or_create(user=request.user, post=post, rating=rating)
            update_post_rating_new.delay(post_id=post.id, rating=rating)
            post_rating.save()
        else:
            update_post_rating_again.delay(post_id=post.id, old_rating=old_rating, rating=rating)
            post_rating.rating = rating
            post_rating.save()

        users_rating = rating

    context = {
        "post": post,
        "users_rating": users_rating,
    }

    return shortcuts.render(request, "post/blocks/post_rate.html", context)
