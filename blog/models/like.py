from django.contrib.auth.models import User
from django.db import models

from .comment import Comment
from .post import Post
from .mixins import CreatedAtMixin


class PostLike(
    CreatedAtMixin,
    models.Model,
):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="posts_likes",
        null=True,
    )

    class Meta:
        db_table = "posts_likes"
        unique_together = ("post", "user")


class CommentLike(
    CreatedAtMixin,
    models.Model,
):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="comments_likes",
        null=True,
    )

    class Meta:
        db_table = "comments_likes"
        unique_together = ("comment", "user")
