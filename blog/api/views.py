from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import generics, permissions

from blog.api.serializers import PostSerializer
from blog.models import Post, Subscription, UserProfile

User = get_user_model()


class PostForAllListApiView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(published="for_all").all()


class PostSubscriptionsListApiView(generics.ListAPIView):
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        subscriptions = Subscription.objects.filter(subscriber=self.request.user.profile).all()
        subscribed_to = [i.subscribed_to.user.username for i in subscriptions]
        return Post.objects.filter(author__username__in=subscribed_to).filter(published="for_subscribers")


class PostMyAllListApiView(generics.ListAPIView):
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).all()


class PostMyDraftsListApiView(generics.ListAPIView):
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).filter(published="draft").all()


class PostMyForAllListApiView(generics.ListAPIView):
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).filter(published="for_all").all()


class PostMyForSubscribersListApiView(generics.ListAPIView):
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).filter(published="for_subscribers").all()


class PostApiView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            queryset = Post.objects.filter(published="for_all").all()
        else:
            post = Post.objects.get(slug=self.kwargs['slug'])
            if post.published == "for_all" or post.author == self.request.user:
                queryset = Post.objects.filter(
                    Q(published="for_all") |
                    Q(author=self.request.user)
                ).all()
            elif post.published == "for_subscribers" and Subscription.objects.filter(subscriber=self.request.user.profile, subscribed_to=UserProfile.objects.get(user=User.objects.get(id=post.author.id))).exists():
                queryset = Post.objects.filter(published="for_subscribers").all()
            else:
                queryset = Post.objects.filter(published="for_all").all()
        return queryset
