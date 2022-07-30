from flask import render_template, current_app, flash, redirect, url_for, request
from blog import db
from blog.models import Users, Posts, Categorys, Tags
from blog.admin.forms import CreateCategoryForm, EditCategoryForm, CreateTagForm, EditTagForm
from flask_babel import _, lazy_gettext as _l
from flask_login import current_user
from slugify import slugify


class BlogAdmin():

    def __init__(self, *args, **kwargs):
        super(BlogAdmin, self).__init__(*args, **kwargs)


    def admin_blog(data):
        if current_user.is_authenticated and current_user.admin:
            nums = {
                'allusers': Users.query.count(),
            'admins': Users.query.filter_by(admin="1").count(),
            'authors': Users.query.filter_by(admin="0").filter_by(author="1").count(),
            'readers': Users.query.filter_by(admin="0").filter_by(author="0").count(),
            'confirmed': Users.query.filter_by(confirmed="1").count(),
            'noconfirmed': Users.query.filter_by(confirmed="0").count(),
            'allposts': Posts.query.count(),
            'publishedposts': Posts.query.filter_by(published="1").count(),
            'inworkposts': Posts.query.filter_by(published="0").count(),
            'allcategorys': Categorys.query.count(),
            'alltags': Tags.query.count()
            }
            users = Users.query.all()
            posts = Posts.query.all()
            categorys = Categorys.query.all()
            tags = Tags.query.all()
            if data == 'allusers':
                title = {'title': _('Admin panel. All users.')}
            if data == 'admins':
                users = Users.query.filter_by(admin="1").all()
                title = {'title': _('Admin panel. Admins.')}
            if data == 'authors':
                users = Users.query.filter_by(admin="0").filter_by(author="1").all()
                title = {'title': _('Admin panel. Authors.')}
            if data == 'readers':
                users = Users.query.filter_by(admin="0").filter_by(author="0").all()
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
            if data == 'allcategorys':
                title = {'title': _('Admin panel. Categorys of posts.')}
            if data == 'alltags':
                title = {'title': _('Admin panel. Tags of posts.')}
            return render_template('admin/blog.html', title=title, users=users, data=data, posts=posts, categorys=categorys, tags=tags, nums=nums, Posts=Posts, Users=Users, Categorys=Categorys, Tags=Tags)
        else:
            flash(_('Please log as admin.'))
            return redirect(url_for('post.indexblog'))



    def create_category(title):
        if current_user.is_authenticated and current_user.admin or current_user.author:
            form = CreateCategoryForm()
            if form.validate_on_submit():
                category = Categorys(name = form.name.data, slug = slugify(form.slug.data))
                if not category.name:
                    flash(_('Please fill in all required fields.'))
                else:
                    if not category.slug:
                        category.slug = slugify(form.name.data)
                    db.session.add(category)
                    db.session.commit()
                    flash(_('Congratulations, category "%(category)s" has been saved.', category=category.name))
                    return redirect(url_for('admin.adminblog', data='allcategorys'))
            return render_template('admin/createeditblog.html', title=title, form=form)
        else:
            flash(_('To create a category of post, please log as admin or author.'))
            if current_user.is_authenticated:
                return redirect(url_for('user.logout'))
            return redirect(url_for('user.login'))


    def edit_category(title, slug):
        if current_user.is_authenticated and current_user.admin:
            form = EditCategoryForm()
            category = Categorys.query.filter_by(slug=slug).first_or_404()
            if form.validate_on_submit():
                newcategory = Categorys.query.filter_by(name=form.name.data).first()
                if not newcategory or newcategory.id == category.id:
                    if not form.name.data:
                        flash(_('Please fill in all required fields.'))
                    else:
                        category.name = form.name.data
                        category.slug = slugify(form.slug.data)
                        if not category.slug:
                            category.slug = slugify(form.name.data)
                        db.session.commit()
                        flash(_('Changes to category "%(category)s" successfully made.', category=category.name))
                        return redirect(url_for('admin.adminblog', data='allcategorys'))
                else:
                    flash(_('A category with the same name has already been created.'))
                    return redirect(url_for('admin.editcategory', slug=category.slug))
            elif request.method == 'GET':
                form.name.data = category.name
                form.slug.data = category.slug
            return render_template('admin/createeditblog.html', title=title, form=form)
        else:
            flash(_('To edit a category of post, please log as admin.'))
            if current_user.is_authenticated:
                return redirect(url_for('user.logout'))
            return redirect(url_for('user.login'))


    def delete_category(slug):
        category = Categorys.query.filter_by(slug=slug).first_or_404()
        postsincategory = Posts.query.filter_by(category_id=category.id).all()
        if current_user.is_authenticated and current_user.admin:
            db.session.delete(category)
            db.session.commit()
            flash(_('Category "%(category)s" successfully delete.', category=category.name))
            for post in postsincategory:
                post.category_id = '1'
                db.session.commit()
            return redirect(url_for('admin.adminblog', data='allcategorys'))
        else:
            flash(_('To delete a category of post, please log as admin.'))
            if current_user.is_authenticated:
                return redirect(url_for('user.logout'))
            return redirect(url_for('user.login'))


    def create_tag(title):
        if current_user.is_authenticated and current_user.admin or current_user.author:
            form = CreateTagForm()
            if form.validate_on_submit():
                tag = Tags(name = form.name.data, slug = slugify(form.slug.data))
                if not tag.name:
                    flash(_('Please fill in all required fields.'))
                else:
                    if not tag.slug:
                        tag.slug = slugify(form.name.data)
                    db.session.add(tag)
                    db.session.commit()
                    flash(_('Congratulations, tag "%(tag)s" has been saved.', tag=tag.name))
                    return redirect(url_for('post.tagsblog'))
            return render_template('admin/createeditblog.html', title=title, form=form)
        else:
            flash(_('To create a tag of post, please log as admin or author.'))
            if current_user.is_authenticated:
                return redirect(url_for('user.logout'))
            return redirect(url_for('user.login'))


    def edit_tag(title, slug):
        if current_user.is_authenticated and current_user.admin:
            form = EditTagForm()
            tag = Tags.query.filter_by(slug=slug).first_or_404()
            if form.validate_on_submit():
                newtag = Tags.query.filter_by(name=form.name.data).first()
                if not newtag or newtag.id == tag.id:
                    if not form.name.data:
                        flash(_('Please fill in all required fields.'))
                    else:
                        tag.name = form.name.data
                        tag.slug = slugify(form.slug.data)
                        if not tag.slug:
                            tag.slug = slugify(form.name.data)
                        db.session.commit()
                        flash(_('Changes to tag "%(tag)s" successfully made.', tag=tag.name))
                        return redirect(url_for('admin.adminblog', data='alltags'))
                else:
                    flash(_('The same tag has already been created.'))
                    return redirect(url_for('admin.edittag', slug=tag.slug))
            elif request.method == 'GET':
                form.name.data = tag.name
                form.slug.data = tag.slug
            return render_template('admin/createeditblog.html', title=title, form=form)
        else:
            flash(_('To edit a tag of post, please log as admin.'))
            if current_user.is_authenticated:
                return redirect(url_for('user.logout'))
            return redirect(url_for('user.login'))


    def delete_tag(slug):
        tag = Tags.query.filter_by(slug=slug).first_or_404()
        if current_user.is_authenticated and current_user.admin:
            db.session.delete(tag)
            db.session.commit()
            flash(_('Tag "%(tag)s" successfully delete.', tag=tag.name))
            return redirect(url_for('admin.adminblog', data='alltags'))
        else:
            flash(_('To delete a tag of post, please log as admin.'))
            if current_user.is_authenticated:
                return redirect(url_for('user.logout'))
            return redirect(url_for('user.login'))
