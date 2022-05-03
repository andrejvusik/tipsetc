from blog.user import bp
from blog.user.utils import BlogUsers
from flask_login import login_required
from flask_mail import Message
from flask_babel import _, lazy_gettext as _l


@bp.route("/login", methods=['GET', 'POST'])
def login():
    title = {'title': _('Account login.')}
    return BlogUsers.login_blog(title)


@bp.route("/confirmemailrequest/<username>", methods=['GET', 'POST'])
@login_required
def confirmemailrequest(username):
    title = {'title': _('Email сonfirmation.')}
    return BlogUsers.confirm_email_request(title, username)


@bp.route("/confirmemail/<token>", methods=['GET', 'POST'])
def confirmemail(token):
    return BlogUsers.confirm_email(token)


@bp.route("/resetpasswordrequest", methods=['GET', 'POST'])
def resetpasswordrequest():
    title = {'title': _('Password reset.')}
    return BlogUsers.reset_password_request(title)


@bp.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resetpassword(token):
    title = {'title': _('Password reset.')}
    return BlogUsers.reset_password(title, token)


@bp.route("/logout")
def logout():
    return BlogUsers.logout_blog()


@bp.route("/reg", methods=['GET', 'POST'])
def reguser():
    title = {'title': _('New user registration.')}
    return BlogUsers.reguser_blog(title)


@bp.route('/<username>')
def user(username):
    title = {'title': _('User profile.')}
    return BlogUsers.user_profil_blog(title, username)


@bp.route('/id/<id>')
def userid(id):
    title = {'title': _('User profile.')}
    return BlogUsers.user_profil_id_blog(title, id)


@bp.route('/<username>/edit', methods=['GET', 'POST'])
@login_required
def edituser(username):
    title = {'title': _('Profile editor.')}
    return BlogUsers.user_edit_blog(title, username)


@bp.route("/<username>/delete")
@login_required
def deleteuser(username):
    return BlogUsers.user_delete_blog(username)


@bp.route('/follow/<username>')
@login_required
def followuser(username):
    return BlogUsers.user_follow_blog(username)


@bp.route('/user/unfollow/<username>')
@login_required
def unfollowuser(username):
    return BlogUsers.user_unfollow_blog(username)
