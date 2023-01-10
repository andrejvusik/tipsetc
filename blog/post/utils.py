from blog import db
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from flask_babel import _, lazy_gettext as _l
from werkzeug.urls import url_parse
from blog.post.forms import CreateEditPostForm, CreateEditPostFormAdmin
from blog.models import Users, Posts, Categorys, Tags, posttag
from slugify import slugify
from guess_language import guess_language
from datetime import datetime


class BlogTags():

    def __init__(self, *args, **kwargs):
        super(BlogTags, self).__init__(*args, **kwargs)

    def edit_post_tags_blog(title, id):
        if current_user.is_authenticated:
            post = Posts.query.filter_by(id=id).first_or_404()
            user = Users.query.filter_by(id=post.users_id).first_or_404()
            tags = Tags.query.all()
            if current_user.username == user.username or current_user.admin:
                return render_template('post/editposttags.html', title=title, post=post, tags=tags)
            else:
                flash(_('You do not have sufficient rights to edit: %(title)s', title=post.title))
                return redirect(url_for('post.post', slug=post.slug))


    def post_assign_tag(postid, tagid):
        if current_user.is_authenticated:
            post = Posts.query.filter_by(id=postid).first()
            user = Users.query.filter_by(id=post.users_id).first_or_404()
            tag = Tags.query.filter_by(id=tagid).first()
            if current_user.username == user.username or current_user.admin:
                post.assign_tag(tag)
                db.session.commit()
                return redirect(url_for('post.editposttags', id=post.id))


    def post_unassign_tag(postid, tagid):
        if current_user.is_authenticated:
            post = Posts.query.filter_by(id=postid).first()
            user = Users.query.filter_by(id=post.users_id).first_or_404()
            tag = Tags.query.filter_by(id=tagid).first()
            if current_user.username == user.username or current_user.admin:
                post.unassign_tag(tag)
                db.session.commit()
                return redirect(url_for('post.editposttags', id=post.id))


class BlogCategorys():

    def __init__(self, *args, **kwargs):
        super(BlogCategorys, self).__init__(*args, **kwargs)

    def create_category_post_blog(name):
        category = Categorys(name=name, slug=slugify(name))
        db.session.add(category)
        db.session.commit()
        return category


class BlogPosts():

    def __init__(self, *args, **kwargs):
        super(BlogPosts, self).__init__(*args, **kwargs)


    def index_blog(title):
        page = request.args.get('page', 1, type=int)
        posts = Posts.query.filter_by(published="1").order_by(Posts.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        defurl = 'post.indexblog'
        paginationlist = {
            'first_url': url_for(defurl, page=1),
            'prev_url': url_for(defurl, page=posts.prev_num),
            'this_url': url_for(defurl, page=posts.page),
            'next_url': url_for(defurl, page=posts.next_num),
            'last_url': url_for(defurl, page=posts.pages),
            'first_lable': 1,
            'prev_lable': posts.prev_num,
            'this_lable': posts.page,
            'next_lable': posts.next_num,
            'last_lable': posts.pages
        }
        return render_template('post/index.html', title=title, posts=posts.items, paginationlist=paginationlist)


    def tags_blog(title):
        tags = Tags.query.all()
        return render_template('post/tags.html', title=title, tags=tags)


    def categorys_blog(title):
        categorys = Categorys.query.all()
        return render_template('post/categorys.html', title=title, categorys=categorys, Posts=Posts)


    def followed_posts_blog(title):
        if current_user.is_authenticated:
            page = request.args.get('page', 1, type=int)
            posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
            defurl = 'post.followedposts'
            paginationlist = {
                'first_url': url_for(defurl, page=1),
                'prev_url': url_for(defurl, page=posts.prev_num),
                'this_url': url_for(defurl, page=posts.page),
                'next_url': url_for(defurl, page=posts.next_num),
                'last_url': url_for(defurl, page=posts.pages),
                'first_lable': 1,
                'prev_lable': posts.prev_num,
                'this_lable': posts.page,
                'next_lable': posts.next_num,
                'last_lable': posts.pages
            }
            if current_user.followed_posts().count() == 0:
                flash(_('You are not subscribed to anyone.'))
                return redirect(url_for('post.indexblog'))
            else:
                return render_template('post/index.html', title=title, posts=posts.items, paginationlist=paginationlist)
        else:
            flash(_('Sign in to your account to view subscriptions.'))
            return redirect(url_for('post.indexblog'))


    def category_posts_blog(slug):
        page = request.args.get('page', 1, type=int)
        category = Categorys.query.filter_by(slug=slug).first_or_404()
        posts = Posts.query.filter_by(published="1").filter_by(category_id=category.id).order_by(Posts.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        countposts = Posts.query.filter_by(published="1").filter_by(category_id=category.id).count()
        paginationlist = {
            'first_url': url_for('post.categoryposts', slug=category.slug, page=1),
            'prev_url': url_for('post.categoryposts', slug=category.slug, page=posts.prev_num),
            'this_url': url_for('post.categoryposts', slug=category.slug, page=posts.page),
            'next_url': url_for('post.categoryposts', slug=category.slug, page=posts.next_num),
            'last_url': url_for('post.categoryposts', slug=category.slug, page=posts.pages),
            'first_lable': 1,
            'prev_lable': posts.prev_num,
            'this_lable': posts.page,
            'next_lable': posts.next_num,
            'last_lable': posts.pages
            }
        if countposts == 0:
            flash(_('There are no posts in the selected category.'))
            return redirect(url_for('post.indexblog'))
        else:
            title = {'title': _('Posts in category: "%(name)s"', name = category.name)}
            return render_template('post/index.html', title=title, posts=posts.items, paginationlist=paginationlist)


    def tag_posts_blog(slug):
        page = request.args.get('page', 1, type=int)
        tag = Tags.query.filter_by(slug=slug).first_or_404()
        posts = tag.posts.filter_by(published="1").order_by(Posts.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        countposts = tag.posts.filter_by(published="1").count()
        paginationlist = {
            'first_url': url_for('post.tagposts', slug=tag.slug, page=1),
            'prev_url': url_for('post.tagposts', slug=tag.slug, page=posts.prev_num),
            'this_url': url_for('post.tagposts', slug=tag.slug, page=posts.page),
            'next_url': url_for('post.tagposts', slug=tag.slug, page=posts.next_num),
            'last_url': url_for('post.tagposts', slug=tag.slug, page=posts.pages),
            'first_lable': 1,
            'prev_lable': posts.prev_num,
            'this_lable': posts.page,
            'next_lable': posts.next_num,
            'last_lable': posts.pages
            }
        if countposts == 0:
            flash(_('No posts associated with the tag: "%(name)s".', name = tag.name))
            return redirect(url_for('post.indexblog'))
        else:
            title = {'title': _('Posts containing tag: "%(name)s"', name = tag.name)}
            return render_template('post/index.html', title=title, posts=posts.items, paginationlist=paginationlist)


    def post_slug_blog(slug):
        if current_user.is_authenticated:
            if current_user.admin or current_user.author:
                post = Posts.query.filter_by(slug=slug).first_or_404()
                return render_template('post/post.html', post=post)
        post = Posts.query.filter_by(slug=slug).filter_by(published=1).first_or_404()
        return render_template('post/post.html', post=post)


    def post_id_blog(id):
        if current_user.is_authenticated:
            if current_user.admin or current_user.author:
                post = Posts.query.filter_by(id=id).first_or_404()
                return render_template('post/post.html', post=post)
        post = Posts.query.filter_by(id=id).filter_by(published=1).first_or_404()
        return render_template('post/post.html', post=post)


    def create_post_blog(title):
        if current_user.is_authenticated:
            if current_user.admin:
                form = CreateEditPostFormAdmin()
                form.set_choices()
            elif current_user.author:
                form = CreateEditPostForm()
                form.set_choices()
            else:
                flash(_('You do not have sufficient rights to create a post.'))
                return redirect(url_for('post.indexblog'))
            if form.validate_on_submit():
                language = guess_language(form.title.data)
                if language == 'UNKNOWN' or len(language) > 5:
                    language = ''
                post = Posts(users_id=current_user.id, title=form.title.data, slug=slugify(form.slug.data), content=form.content.data, published="0", language=language)
                if form.category.data:
                    category = Categorys.query.filter_by(name=form.category.data).first()
                    if not category:
                        category = BlogCategorys.create_category_post_blog(name=form.category.data)
                    post.category_id = category.id
                elif not form.category.data:
                    post.category_id = '1'
                if current_user.admin:
                    post.published = form.published.data
                    authorpost = Users.query.filter_by(username=form.author.data).first()
                    if not authorpost:
                        flash(_('The user with this ID was not found. Authorship assigned %(username)s.', username=current_user.username))
                        post.users_id = current_user.id
                    else:
                        post.users_id = authorpost.id
                if not post.title or not post.content:
                    flash(_('Please fill in all required fields.'))
                else:
                    if not post.slug:
                        post.slug = slugify(form.title.data)
                    db.session.add(post)
                    db.session.commit()
                    flash(_('Congratulations, your post "%(title)s" has been saved.', title=post.title))
                    if form.edittagsaftersaving.data:
                        return redirect(url_for('post.editposttags', id = post.id))
                    return redirect(url_for('post.post', slug=post.slug))
            return render_template('post/createpost.html', title=title, form=form)
        else:
            flash(_('To create an post, please log in to your account.'))
            return redirect(url_for('user.login'))


    def edit_post_blog(title, id):
        if current_user.is_anonymous:
            flash(_('Log in to your account to edit posts.'))
            return redirect(url_for('post.postid', id=id))
        if current_user.admin:
            form = CreateEditPostFormAdmin()
            form.set_choices()
        elif current_user.author:
            form = CreateEditPostForm()
            form.set_choices()
        else:
            flash(_('You do not have sufficient rights to edit posts.'))
            return redirect(url_for('post.postid', id=id))
        post = Posts.query.filter_by(id=id).first_or_404()
        tags = Tags.query.all()
        if form.validate_on_submit():
            language = guess_language(form.title.data)
            if language == 'UNKNOWN' or len(language) > 5:
                language = ''
            if current_user.admin:
                post.published = form.published.data
                postauthors = Users.query.filter_by(username=form.author.data).first()
                if not postauthors:
                    flash(_('Please check the user ID. User with this ID was not found.'))
                    return redirect(url_for('post.editpost', id=post.id))
                else:
                    post.users_id = postauthors.id
            post.title = form.title.data
            if not form.slug:
                post.slug = slugify(form.title.data)
            else:
                post.slug = slugify(form.slug.data)
            post.content = form.content.data
            if form.category.data:
                newcategory = Categorys.query.filter_by(name=form.category.data).first()
                if not newcategory:
                    newcategory = BlogCategorys.create_category_post_blog(name=form.category.data)
                post.category_id = newcategory.id
            elif not form.category.data:
                post.category_id = '1'
            post.language = language
            db.session.commit()
            flash(_('Changes to "%(title)s" successfully made.', title=post.title))
            if form.edittagsaftersaving.data:
                return redirect(url_for('post.editposttags', id = post.id))
            return redirect(url_for('post.post', slug=post.slug))
        elif request.method == 'GET':
            if current_user.admin:
                form.author.data = post.author.username
                form.published.data = post.published
            form.title.data = post.title
            form.slug.data = post.slug
            form.content.data = post.content
            if post.category:
                form.category.data = post.category.name
        return render_template('post/editpost.html', title=title, form=form, post=post, tags=tags)


    def post_publish_slug_blog(id):
        if current_user.is_authenticated:
            post = Posts.query.filter_by(id=id).first_or_404()
            if current_user.admin:
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('post.post', slug=post.slug)
                if post.published:
                    post.published = '0'
                    flash('Post "{}" unpublished'.format(post.title))
                else:
                    post.published = '1'
                    post.timestamp = datetime.utcnow()
                    flash('Post "{}" published'.format(post.title))
                db.session.commit()
                return redirect(next_page)
            flash(_('You do not have sufficient rights to publishing: %(title)s', title=post.title))
            return redirect(url_for('main.index'))



    def post_delete_blog(id):
        if current_user.is_authenticated:
            post = Posts.query.filter_by(id=id).first_or_404()
            user = Users.query.filter_by(id=post.users_id).first_or_404()
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            if current_user.username == user.username or current_user.admin:
                db.session.delete(post)
                db.session.commit()
                flash('Post "{}" deleted'.format(post.title))
                return redirect(next_page)
            flash(_('You do not have sufficient rights to delete: %(title)s', title=post.title))
            return redirect(url_for('post.post', slug=post.slug))
