from django.urls import path

from . import views

urlpatterns = [
    path("", views.posts, name="posts"),
    path("posts", views.posts, name="posts"),
    path("posts/<param>", views.posts, name="posts"),
    path("posts/post/<slug>", views.post_view, name="post_view"),
    path("search_publish_posts", views.search_publish_posts, name="search_publish_posts"),

    path("auth/signin", views.user_signin, name="user_signin"),
    path("auth/signup", views.user_signup, name="user_signup"),
    path("auth/logout", views.user_logout, name="user_logout"),
]
