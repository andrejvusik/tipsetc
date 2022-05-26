from blog.post import bp
from blog.post.utils import BlogPosts
from flask_login import login_required
from flask_babel import _


@bp.route("/")
@bp.route("/index")
def indexblog():
    title = {'title': _('Resent posts.')}
    return BlogPosts.index_blog(title)


@bp.route("/followed/posts")
@login_required
def followedposts():
    title = {'title': _('Subscriptions.')}
    return BlogPosts.followed_posts_blog(title)

@bp.route("/category/<slug>")
def categoryposts(slug):
    return BlogPosts.category_posts_blog(slug)


@bp.route("/<slug>")
def post(slug):
    return BlogPosts.post_slug_blog(slug)


@bp.route("/id/<id>")
def postid(id):
    return BlogPosts.post_id_blog(id)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def createpost():
    title = {'title': _('Create new post.')}
    return BlogPosts.create_post_blog(title)


@bp.route('/id/<id>/edit', methods=('GET', 'POST'))
@login_required
def editpost(id):
    title = {'title': _('Edit post: ')}
    return BlogPosts.edit_post_blog(title, id)


@bp.route("/id/<id>/delete")
@login_required
def deletepost(id):
    return BlogPosts.post_delete_blog(id)
