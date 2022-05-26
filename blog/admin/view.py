from blog.admin import bp
from blog.admin.utils import BlogAdmin
from flask_login import login_required
from flask_babel import _


@bp.route("/blog/<data>")
@login_required
def adminblog(data):
    return BlogAdmin.admin_blog(data)

@bp.route("/blog/createcategory", methods=('GET', 'POST'))
@login_required
def createcategory():
    title = {'title': _('Admin panel. Creating a blog post category.')}
    return BlogAdmin.create_category(title)

@bp.route("/blog/editcategory/<slug>", methods=('GET', 'POST'))
@login_required
def editcategory(slug):
    title = {'title': _('Admin panel. Editing a blog post category.')}
    return BlogAdmin.edit_category(title, slug)

@bp.route("/blog/deletecategory/<slug>")
@login_required
def deletecategory(slug):
    return BlogAdmin.delete_category(slug)
