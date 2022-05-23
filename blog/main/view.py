from blog import db
from blog.main import bp
from flask import g, request
from flask_login import current_user
from flask_babel import _, get_locale
from datetime import datetime
from blog.post.utils import BlogPosts
from blog.models import Posts, Categorys


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())
    g.categorys = Categorys.query.all()
    g.posts = Posts


@bp.route("/")
@bp.route("/index")
def index():
    title = {'title': _('Resent posts.')}
    return BlogPosts.index_blog(title)
