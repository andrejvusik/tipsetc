from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.conf import settings

from .models import Post


# Create your views here.

def posts(request, param=""):
    params = {
        "": Post.objects.filter(published="for_all"),
        "all_publish_posts": Post.objects.filter(published="for_all"),
        "exception": Post.objects.filter(published="for_all"),
    }
    titles = {
        "": "Latest Published Posts",
        "all_publish_posts": "Latest Published Posts",
        "exception": f"This page \"{param}\" does not exist. Below are latest Published Posts.",
    }
    if request.user.is_authenticated:
        params["my_posts"] = Post.objects.filter(author=request.user)
        titles["my_posts"] = "My Posts"
    if not param in params:
        param = "exception"
    q_posts = params[param].order_by("-updated_at")[:settings.COUNT_OF_POST_ON_PAGE]
    title = titles[param]
    context = {
        "posts": q_posts,
        "settings": settings,
        "title": title,
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
