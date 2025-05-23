# from django.shortcuts import render
from django.http.response import HttpResponse
from django.template import loader

from .models import Post


# Create your views here.


def index(request):
    posts = Post.objects.order_by("-updated_at")[:5]
    template = loader.get_template("index.html")
    context = {"posts": posts}
    return HttpResponse(template.render(context, request))
