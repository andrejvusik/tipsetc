from blog import db
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from flask_babel import _, lazy_gettext as _l
from blog.models import Users, Posts
from blog.user.forms import LoginForm, RegistrationForm, EditProfilForm, ResetPasswordRequestForm, ResetPasswordForm
from blog.user.emails import send_password_reset_email, send_reg_new_user, send_confirm_email
from werkzeug.urls import url_parse
from slugify import slugify
from datetime import datetime


class BlogUsers():

    def __init__(self, *args, **kwargs):
        super(BlogUsers, self).__init__(*args, **kwargs)

    def login_blog(title):
        if current_user.is_authenticated:
            flash(_('You are already logged in as: "%(username)s"',
                  username=current_user.username))
            return redirect(url_for('post.indexblog'))
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash(_('Please check your email address or password.'))
                return redirect(url_for('user.login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('post.indexblog')
                return redirect(next_page)
            flash(_('You are logged in as: "%(username)s"',
                  username=current_user.username))
            return redirect(url_for('post.indexblog'))
        return render_template('user/login.html', title=title, form=form)

    def confirm_email_request(title, username):
        user = Users.query.filter_by(username=username).first()
        if current_user.is_authenticated:
            if user.username == current_user.username or current_user.admin:
                send_confirm_email(user)
                flash(_('Check your email to verify your account.'))
                return redirect(url_for('user.user', username=user.username))
            else:
                flash(_('Something went wrong.'))
                return redirect(url_for('post.indexblog'))
        else:
            flash(_('To confirm your email, you must login.'))
            return redirect(url_for('user.login'))

    def confirm_email(token):
        if current_user.is_authenticated:
            user = Users.verify_confirmation_token(token)
            if user.username != current_user.username:
                flash(_('The verification link is invalid or has expired.'))
                return redirect(url_for('post.indexblog'))
            elif user.confirmed:
                flash(_('Your account has already been verified.'))
                return redirect(url_for('user.user', username=user.username))
            elif user.username == current_user.username:
                current_user.confirmed = True
                db.session.commit()
                flash(_('Congratulations! Your account has been verified.'))
                return redirect(url_for('user.user', username=current_user.username))
        else:
            flash(_('To confirm your email, you must login.'))
            return redirect(url_for('user.login'))

    def reset_password_request(title):
        if current_user.is_authenticated:
            flash(_('You are already logged in as: "%(username)s"',
                  username=current_user.username))
            return redirect(url_for('post.indexblog'))
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                send_password_reset_email(user)
                flash(_('Check your email for password reset instructions.'))
                return redirect(url_for('user.login'))
            else:
                flash(_('Check the email you entered.'))
        return render_template('user/resetpasswordrequest.html', title=title, form=form)

    def reset_password(title, token):
        if current_user.is_authenticated:
            flash(_('You are already logged in as: "%(username)s"',
                  username=current_user.username))
            return redirect(url_for('post.indexblog'))
        user = Users.verify_reset_password_token(token)
        if not user:
            return redirect(url_for('post.indexblog'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form. password.data)
            db.session.commit()
            flash(_('Your password has been reset.'))
            return redirect(url_for('user.login'))
        return render_template('user/resetpassword.html', title=title, user=user, form=form)

    def logout_blog():
        logout_user()
        return redirect(url_for('post.indexblog'))

    def reguser_blog(title):
        if current_user.is_authenticated:
            flash(_('You are already logged in as: "%(username)s"', username=current_user.username))
            return redirect(url_for('post.indexblog'))
        form = RegistrationForm()
        if form.validate_on_submit():
            if form.agree_terms.data:
                user = Users(username=slugify(form.username.data), full_name=form.full_name.data, email=form.email.data, telegram=form.telegram.data,
                             show_personal=form.show_personal.data, admin="0", author="0", confirmed="0", about_me=form.about_me.data, registered=datetime.utcnow())
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                send_reg_new_user(user)
                login_user(user)
                flash(
                    _('Congratulations, you "%(username)s" have become a registered user.', username=user.username))
                return redirect(url_for('user.user', username=user.username))
            else:
                flash(_('Please accept the terms of the user agreement. Thanks.'))
        return render_template('user/reguser.html', title=title, form=form)

    def user_edit_blog(title, username):
        form = EditProfilForm()
        user = Users.query.filter_by(username=username).first_or_404()
        if current_user.username == user.username or current_user.admin:
            if form.validate_on_submit():
                newauthor = Users.query.filter_by(id=form.userid.data).first()
                if not newauthor or newauthor.id == user.id:
                    user.id = form.userid.data
                    user.username = slugify(form.username.data)
                    user.full_name = form.full_name.data
                    user.email = form.email.data
                    user.telegram = form.telegram.data
                    user.show_personal = form.show_personal.data
                    user.about_me = form.about_me.data
                    user.admin = form.admin.data
                    user.author = form.author.data
                    user.confirmed = form.confirmed.data
                    if not user.registered:
                        user.registered = user.last_seen
                    db.session.commit()
                    flash(_('The profile changes have been made.'))
                    return redirect(url_for('user.user', username=user.username))
                else:
                    flash(_('The user with this ID is already registered.'))
                    return redirect(url_for('user.edituser', username=user.username))
            elif request.method == 'GET':
                form.userid.data = user.id
                form.username.data = user.username
                form.full_name.data = user.full_name
                form.email.data = user.email
                form.telegram.data = user.telegram
                form.show_personal.data = user.show_personal
                form.about_me.data = user.about_me
                form.admin.data = user.admin
                form.author.data = user.author
                form.confirmed.data = user.confirmed
            return render_template('user/edituser.html', title=title, form=form, user=user)
        flash(_('You do not have enough rights to change the user profile: $(username)s',
              username=user.username))
        return redirect(url_for('user.user', username=user.username))

    def user_profil_blog(title, username):
        user = Users.query.filter_by(username=username).first_or_404()
        page = request.args.get('page', 1, type=int)
        posts = user.posts.order_by(Posts.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
        nums = user.posts.count()
        defurl = 'user.user'
        paginationlist = {
            'first_url': url_for(defurl, username=user.username, page=1),
            'prev_url': url_for(defurl, username=user.username, page=posts.prev_num),
            'this_url': url_for(defurl, username=user.username, page=posts.page),
            'next_url': url_for(defurl, username=user.username, page=posts.next_num),
            'last_url': url_for(defurl, username=user.username, page=posts.pages),
            'first_lable': 1,
            'prev_lable': posts.prev_num,
            'this_lable': posts.page,
            'next_lable': posts.next_num,
            'last_lable': posts.pages
        }
        return render_template('user/user.html', title=title, user=user, posts=posts.items, nums=nums, paginationlist=paginationlist)

    def user_profil_id_blog(title, id):
        user = Users.query.filter_by(id=id).first_or_404()
        page = request.args.get('page', 1, type=int)
        posts = user.posts.order_by(Posts.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
        nums = user.posts.count()
        defurl = 'user.userid'
        paginationlist = {
            'first_url': url_for(defurl, id=user.id, page=1),
            'prev_url': url_for(defurl, id=user.id, page=posts.prev_num),
            'this_url': url_for(defurl, id=user.id, page=posts.page),
            'next_url': url_for(defurl, id=user.id, page=posts.next_num),
            'last_url': url_for(defurl, id=user.id, page=posts.pages),
            'first_lable': 1,
            'prev_lable': posts.prev_num,
            'this_lable': posts.page,
            'next_lable': posts.next_num,
            'last_lable': posts.pages
        }
        return render_template('user/user.html', title=title, user=user, posts=posts.items, nums=nums, paginationlist=paginationlist)

    def user_delete_blog(username):
        user = Users.query.filter_by(username=username).first_or_404()
        usersposts = Posts.query.filter_by(users_id=user.id).all()
        if current_user.username == user.username or current_user.admin:
            db.session.delete(user)
            db.session.commit()
            flash(_('User "%(username)s" has been deleted.', username=user.username))
            for post in usersposts:
                post.users_id = '1'
                db.session.commit()
            return redirect(url_for('main.index'))
        flash(_('You do not have sufficient rights to delete a user: %(username)s.', username=user.username))
        return redirect(url_for('user.user', username=user.username))

    def user_follow_blog(username):
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash(_('User "%(username)s" is not found.', username=username))
            return redirect(url_for('index'))
        if user == current_user:
            flash(_('You cannot subscribe to yourself.'))
            return redirect(url_for('user.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('You followed: "%(username)s"!', username=username))
        return redirect(url_for('user.user', username=username))

    def user_unfollow_blog(username):
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash(_('User "%(username)s" is not found.', username=username))
            return redirect(url_for('post.indexblog'))
        if user == current_user:
            flash(_('You cannot unsubscribe to yourself.'))
            return redirect(url_for('user.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You unfollowed: "%(username)s".', username=username))
        return redirect(url_for('user.user', username=username))
