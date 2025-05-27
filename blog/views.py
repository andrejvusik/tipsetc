from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render
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
    # q_posts = params[param].order_by("-updated_at")[:settings.COUNT_OF_POST_ON_PAGE]
    q_posts = params[param].order_by("-updated_at")

    page_number = request.GET.get('page', 1)
    paginator = Paginator(q_posts, settings.COUNT_OF_POST_ON_PAGE)
    page_obj = paginator.get_page(page_number)

    title = titles[param]
    context = {
        "posts": page_obj,
        "count_posts": q_posts.count(),
        "settings": settings,
        "title": title,
        "param": param,
        "has_next": page_obj.has_next(),
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
    }

    # if request.headers.get("HX-Request") is True:
    if page_number == 1:
        return render(request, "post/posts.html", context)

    return render(request, "post/blocks/posts_item.html", context)


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

def post_view(request, slug):
    result = get_object_or_404(Post, slug=slug)
    context = {
        "post": result,
        "settings": settings,
    }
    return render(request, "post/post.html", context)
