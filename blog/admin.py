from django.contrib import admin
from django.utils.html import format_html

from blog import models


# Register your models here.


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "created_at",
        "updated_at",
        "published",
    )
    list_filter = (
        "author",
        "published",
    )
    search_fields = (
        "title",
        "content",
    )
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "content",
                    (
                        "author",
                        "published",
                    ),
                ),
            },
        ),
        (
            "Tags",
            {
                "fields": ("tags",),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (None, {"fields": ("name",)}),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "get_avatar",
        "user__username",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__username",)
    ordering = ("user__username",)

    @admin.display(empty_value="-")
    def get_avatar(self, user_profile):
        if not user_profile.avatar:
            return None
        return format_html(
            f'<img src="{user_profile.avatar}" width="60" height="60" />'
        )

    get_avatar.short_description = "Avatar"
