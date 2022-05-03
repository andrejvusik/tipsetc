from blog.admin import bp
from blog.admin.utils import BlogAdmin
from flask_login import login_required


@bp.route("/blog/<data>")
@login_required
def adminblog(data):
    return BlogAdmin.admin_blog(data)
