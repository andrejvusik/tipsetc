from django.urls import path

from blog.api import views


urlpatterns = [
    path('posts/for/all', views.PostForAllListApiView.as_view(), name='api_posts_for_all'),
    path('posts/subscriptions', views.PostSubscriptionsListApiView.as_view(), name='api_posts_subscriptions'),
    path('posts/my/all', views.PostMyAllListApiView.as_view(), name='api_posts_my_all'),
    path('posts/my/drafts', views.PostMyDraftsListApiView.as_view(), name='api_posts_my_drafts'),
    path('posts/my/for/all', views.PostMyForAllListApiView.as_view(), name='api_posts_my_for_all'),
    path('posts/my/for/subscribers', views.PostMyForSubscribersListApiView.as_view(), name='api_posts_my_for_subscribers'),
    path('posts/post/<str:slug>', views.PostApiView.as_view(), name='post_api_view'),
]