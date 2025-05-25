from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.conf import settings

from .models import Post


# Create your views here.


def latest_posts(request):
    posts = Post.objects.filter(published="for_all").order_by("-updated_at")[:settings.COUNT_OF_POST_ON_PAGE]
    title = "Latest Published Posts"
    context = {
        "posts": posts,
        "settings": settings,
        "title": title,
    }
    return render(request, "post/posts.html", context)

def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by("-updated_at")[:settings.COUNT_OF_POST_ON_PAGE]
    title = "My Posts"
    context = {
        "posts": posts,
        "settings": settings,
        "title": title
    }
    return render(request, "post/posts.html", context)

def search_publish_posts(request):
    query = request.GET.get('query')
    results = []
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by("-updated_at")[:settings.SEARCH_RESULTS_LIMIT]

    return render(
        request,
        "post/blocks/search_publish_posts.html",
        {"results": results, "query": query},
    )
