import re

from django import shortcuts
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.conf import settings

from blog.forms import CreateEditPostForm
from blog.models import Post


User = get_user_model()

def text_slugify(text, test_model):
    if not text:
        return None
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s+]', '-', text)
    text = text.lower()
    while True:
        if test_model.objects.filter(slug=text).count() > 0:
            text = text + "-1"
        else:
            break
    return text


def posts(request, param="all_publish_posts"):
    params = {
        "all_publish_posts": Post.objects.filter(published="for_all"),
        "exception": Post.objects.filter(published="for_all"),
    }
    titles: dict[str, str] = {
        "all_publish_posts": "Latest Published Posts",
        "exception": f"This page \"{param}\" does not exist. Below are latest Published Posts.",
    }
    if User.objects.filter(username=param).exists():
        params[f"{param}"] = Post.objects.filter(author=User.objects.get(username=param)).filter(published="for_all")
        titles[f"{param}"] = f"Posts by {param}"

    if request.user.is_authenticated:
        params["my_posts"] = Post.objects.filter(author=request.user)
        params["my_drafts"] = Post.objects.filter(author=request.user).filter(published="draft")
        params["my_posts_for_all"] = Post.objects.filter(author=request.user).filter(published="for_all")
        params["my_posts_for_subscribers"] = Post.objects.filter(author=request.user).filter(published="for_subscribers")
        titles["my_posts"] = "My Posts"
        titles["my_drafts"] = "My drafts"
        titles["my_posts_for_all"] = "My posts published for all"
        titles["my_posts_for_subscribers"] = "My posts published for subscribers"
    if not param in params:
        param = "exception"
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
        return shortcuts.render(request, "post/posts.html", context)

    return shortcuts.render(request, "post/blocks/posts_item.html", context)


def search_publish_posts(request):
    query = request.GET.get('query')
    results = []
    if query:
        results = Post.objects.filter(published="for_all").filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by("-updated_at")[:settings.SEARCH_RESULTS_LIMIT]

    return shortcuts.render(
        request,
        "post/blocks/search_publish_posts.html",
        {"results": results, "query": query},
    )

@login_required
def post_create(request):
    if request.method == "POST":
        form = CreateEditPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            slug = text_slugify(title, Post)
            content = form.cleaned_data["content"]
            published = form.cleaned_data["published"]

            new_post = Post(
                title=title,
                slug=slug,
                content=content,
                published=published,
                author=request.user,
            )

            new_post.save()
            context = {
                "post": new_post,
                "settings": settings,
            }
            messages.success(request, f'Post "{new_post.title}" saved successfully with the status: "{new_post.published_status}".')
            return shortcuts.render(request, "post/post_view.html", context)
    form = CreateEditPostForm()
    context = {
        "settings": settings,
        "form": form,
        "Post": Post,
    }
    return shortcuts.render(request, "post/post_create.html", context)

def post_view(request, slug):
    post = shortcuts.get_object_or_404(Post, slug=slug)
    if post.published == "for_all" or post.author == request.user:
        context = {
            "post": post,
            "settings": settings,
        }
        return shortcuts.render(request, "post/post_view.html", context)
    else:
        messages.success(request, "This post is not published yet.")
        return shortcuts.redirect("posts", param="all_publish_posts")

@login_required
def post_edit(request, slug):
    post = shortcuts.get_object_or_404(Post, slug=slug)
    form = CreateEditPostForm(request.POST, post)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            slug = text_slugify(title, Post)
            content = form.cleaned_data["content"]
            published = form.cleaned_data["published"]

            post.title = title
            post.slug = slug
            post.content = content
            post.published = published

            post.save()

            messages.success(request, f'Post "{post.title}" successfully edit.')
            return shortcuts.redirect("post_view", slug=post.slug)
    context = {
        "settings": settings,
        "post": post,
        "form": form,
    }
    return shortcuts.render(request, "post/post_edit.html", context)

@login_required
def post_delete(request, slug):
    post = shortcuts.get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        post.delete()
        messages.success(request, f'Post "{post.title}" deleted successfully.')
        return shortcuts.redirect("posts", param="my_posts")
    else:
        messages.error(request, "No found the object to delete.")
        return shortcuts.redirect("post_view", slug=slug)

@login_required
def post_status_change(request, slug, param):
    post = shortcuts.get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        post.published = param
        post.save()
        messages.success(request, f'The status of the post "{ post.title }" has been successfully changed on "{ post.published_status }".')
        return shortcuts.redirect("post_view", slug=post.slug)
    else:
        messages.error(request, "No found the object to change.")
        return shortcuts.redirect("post_view", slug=post.slug)
