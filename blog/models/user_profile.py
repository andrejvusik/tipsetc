from django.contrib.auth import get_user_model
from django.db import models

from . import mixins

User = get_user_model()


class UserProfile(mixins.CreatedAtMixin, mixins.UpdatedAtMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return f"{self.user.username}'s profile"
