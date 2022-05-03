
from blog import db
from blog.main import bp
from flask import g
from flask_login import current_user
from flask_babel import _, get_locale
from blog.post.utils import BlogPosts
from datetime import datetime


@bp.before_app_request
def before_request():
    g.locale = str(get_locale())
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route("/")
@bp.route("/index")
def index():
    title = {'title': _('Resent posts.')}
    return BlogPosts.index_blog(title)
