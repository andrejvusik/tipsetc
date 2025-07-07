from django.db import models

from . import mixins
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(
    mixins.CreatedAtMixin,
    mixins.UpdatedAtMixin,
    models.Model,
):
    PUBLISH_STATUS = [
        ("draft", "Draft"),
        ("for_subscribers", "Published for subscribers"),
        ("for_all", "Published for All"),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, allow_unicode=True, null=True, blank=True)
    content = models.TextField(db_index=True, null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="posts"
    )
    published = models.CharField(max_length=16, choices=PUBLISH_STATUS, null=False)

    tags = models.ManyToManyField("Tag", related_name="posts", blank=True)

    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title

    @property
    def published_status(self):
        post_publish_status = {x[0]: x[1] for x in self.PUBLISH_STATUS}
        return post_publish_status[str(self.published)]

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    def is_liked_by(self, user: User) -> bool:
        return self.likes.filter(user=user).exists()

    @property
    def rating(self) -> float | None:
        return self.users_rating.filter(rating__isnull=False).aggregate(avg=models.Avg("rating"))["avg"] or None
