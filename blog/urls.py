from django.urls import path

from . import views

urlpatterns = [
    path("", views.posts, name="posts"),
    path("posts", views.posts, name="posts"),
    path("posts/view/<param>", views.posts, name="posts"),

    path("posts/post/create", views.post_create, name="post_create"),
    path("posts/post/view/<slug>", views.post_view, name="post_view"),
    path("posts/post/edit/<slug>", views.post_edit, name="post_edit"),
    path("posts/post/delete/<slug>", views.post_delete, name="post_delete"),
    path("posts/post/comments/<slug>", views.post_add_comment, name="post_add_comment"),
    path("posts/post/status/change/<slug>/<param>", views.post_status_change, name="post_status_change"),

    path("posts/comment/delete/<int:id>", views.post_delete_comment, name="post_delete_comment"),

    path("like/<obj>/<int:object_id>", views.toggle_like, name="toggle_like"),

    path("search_publish_posts", views.search_publish_posts, name="search_publish_posts"),

    path("auth/signin", views.user_signin, name="user_signin"),
    path("accounts/login/", views.user_signin, name="user_signin"),
    path("auth/signup", views.user_signup, name="user_signup"),
    path("auth/logout", views.user_logout, name="user_logout"),
]
