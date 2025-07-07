from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from . import mixins, Post

User = get_user_model()


class PostRating(mixins.CreatedAtMixin, models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts_rating",
        null=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="users_rating",
        null=False,
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        db_table = "post_rating"
        unique_together = ("user", "post")

