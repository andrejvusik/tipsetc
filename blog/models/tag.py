from django.db import models

from . import mixins


class Tag(
    mixins.CreatedAtMixin,
    mixins.UpdatedAtMixin,
    models.Model,
):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.name
