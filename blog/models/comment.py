from django.contrib.auth.models import User
from django.db import models

from .mixins import CreatedAtMixin

class Comment(
    CreatedAtMixin,
    models.Model
):
    content = models.TextField(
        null=False,
        blank=False,
    )

    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="comments",
        null=False,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
    )

    class Meta:
        db_table = "comments"

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    def is_liked_by(self, user: User) -> bool:
        return self.likes.filter(user=user).exists()
