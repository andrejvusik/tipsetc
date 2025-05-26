from django.urls import path

from . import views

urlpatterns = [
    path("", views.posts, name="posts"),
    path("posts", views.posts, name="posts"),
    path("posts/<param>", views.posts, name="posts"),
    path("search_publish_posts", views.search_publish_posts, name="search_publish_posts"),
]
