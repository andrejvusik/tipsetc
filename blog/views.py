from django.shortcuts import render
from django.conf import settings


from .models import Post


# Create your views here.


def index(request):
    posts = Post.objects.filter(published="for_all").order_by("-updated_at")[:5]
    context = {"posts": posts, "settings": settings}
    return render(request, "index.html", context)
