from django.urls import path

from . import views

urlpatterns = [
    path("", views.latest_posts, name="latest_posts"),
    path("my_posts", views.my_posts, name="my_posts"),
    path("search_publish_posts", views.search_publish_posts, name="search_publish_posts"),
]
