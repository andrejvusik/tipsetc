from flask import render_template, current_app
from flask_babel import _, lazy_gettext as _l
from blog.models import Users, Posts


class BlogAdmin():

    def __init__(self, *args, **kwargs):
        super(BlogAdmin, self).__init__(*args, **kwargs)

    def admin_blog(data):
        nums = {
            'allusers': Users.query.count(),
            'admins': Users.query.filter_by(admin="1").count(),
            'authors': Users.query.filter_by(admin="0").filter_by(author="1").count(),
            'readers': Users.query.filter_by(admin="0").filter_by(author="0").count(),
            'confirmed': Users.query.filter_by(confirmed="1").count(),
            'noconfirmed': Users.query.filter_by(confirmed="0").count(),
            'allposts': Posts.query.count(),
            'publishedposts': Posts.query.filter_by(published="1").count(),
            'inworkposts': Posts.query.filter_by(published="0").count()
        }
        users = Users.query.all()
        posts = Posts.query.all()
        if data == 'allusers':
            title = {'title': _('Admin panel. All users.')}
        if data == 'admins':
            users = Users.query.filter_by(admin="1").all()
            title = {'title': _('Admin panel. Admins.')}
        if data == 'authors':
            users = Users.query.filter_by(
                admin="0").filter_by(author="1").all()
            title = {'title': _('Admin panel. Authors.')}
        if data == 'readers':
            users = Users.query.filter_by(
                admin="0").filter_by(author="0").all()
            title = {'title': _('Admin panel. Readers.')}
        if data == 'confirmed':
            users = Users.query.filter_by(confirmed="1").all()
            title = {'title': _('Admin panel. Verified users.')}
        if data == 'noconfirmed':
            users = Users.query.filter_by(confirmed="0" or None).all()
            title = {'title': _('Admin panel. Unverified users.')}
        if data == 'allposts':
            title = {'title': _('Admin panel. All posts.')}
        if data == 'publishedposts':
            posts = Posts.query.filter_by(published="1").all()
            title = {'title': _('Admin panel. Published posts.')}
        if data == 'inworkposts':
            posts = Posts.query.filter_by(published="0").all()
            title = {'title': _('Admin panel. Posts in progress.')}
        return render_template('admin/usersandpostsblog.html', title=title, users=users, data=data, posts=posts, nums=nums, Posts=Posts, Users=Users)
