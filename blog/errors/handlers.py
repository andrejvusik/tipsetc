from flask import render_template
from blog import db
from blog.errors import bp
from flask_babel import _


@bp.app_errorhandler(404)
def notfounderror(error):
    title = {'title': _('Error: "404"')}
    return render_template('errors/404.html', title=title), 404


@bp.app_errorhandler(500)
def internalerror(error):
    title = {'title': _('Error: "500"')}
    db.session.rollback()
    return render_template('errors/500.html', title=title), 500
