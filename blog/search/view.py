from blog.search import bp
from flask import g,request
from flask_babel import _
from blog.search.forms import SearchForm
from blog.search.utils import BlogSearch


@bp.before_app_request
def before_request():
    g.search_form = SearchForm()


@bp.route("/posts")
def search():
    title = {'title': _('Search results for the request: "%(searchrequest)s".', searchrequest=g.search_form.q.data)}
    return BlogSearch.search_blog(title)
