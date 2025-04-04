from blog.post import bp
from blog.post.utils import BlogTags, BlogPosts
from flask_login import login_required
from flask_babel import _


@bp.route("/")
@bp.route("/index")
def indexblog():
    title = {'title': _('Resent posts.')}
    return BlogPosts.index_blog(title)


@bp.route("/tags")
def tagsblog():
    title = {'title': _('Tags.')}
    return BlogPosts.tags_blog(title)


@bp.route("/categorys")
def categorysblog():
    title = {'title': _('Categorys.')}
    return BlogPosts.categorys_blog(title)


@bp.route("/followed/posts")
@login_required
def followedposts():
    title = {'title': _('Subscriptions.')}
    return BlogPosts.followed_posts_blog(title)


@bp.route("/category/<slug>")
def categoryposts(slug):
    return BlogPosts.category_posts_blog(slug)


@bp.route("/tag/<slug>")
def tagposts(slug):
    return BlogPosts.tag_posts_blog(slug)


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


@bp.route("/id/<id>/publish")
@login_required
def publishpost(id):
    return BlogPosts.post_publish_slug_blog(id)


@bp.route('/id/<id>/edit', methods=('GET', 'POST'))
@login_required
def editpost(id):
    title = {'title': _('Edit post: ')}
    return BlogPosts.edit_post_blog(title, id)


@bp.route("/id/<id>/delete")
@login_required
def deletepost(id):
    return BlogPosts.post_delete_blog(id)



@bp.route('/id/<id>/edittags', methods=('GET', 'POST'))
@login_required
def editposttags(id):
    title = {'title': _('Edit tags. Post: ')}
    return BlogTags.edit_post_tags_blog(title, id)


@bp.route('/id/<postid>/assigntag/<tagid>', methods=('GET', 'POST'))
@login_required
def assigntag(postid, tagid):
    return BlogTags.post_assign_tag(postid, tagid)


@bp.route('/id/<postid>/unassigntag/<tagid>', methods=('GET', 'POST'))
@login_required
def unassigntag(postid, tagid):
    return BlogTags.post_unassign_tag(postid, tagid)
