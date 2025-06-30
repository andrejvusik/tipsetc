from django.db import models

from .user_profile import UserProfile
from .mixins import CreatedAtMixin


class Subscription(
    CreatedAtMixin,
    models.Model,
):
    subscriber = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    subscribed_to = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="subscribers",
    )

    class Meta:
        db_table = "subscription"
        verbose_name_plural = "subscriptions"
        unique_together = ("subscriber", "subscribed_to")

    def __str__(self):
        return f"{self.subscriber} -> {self.subscribed_to}"