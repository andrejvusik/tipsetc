from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from blog import db, login, whooshee
from slugify import slugify


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    telegram = db.Column(db.String(128), index = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Posts', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(256))
    registered = db.Column(db.DateTime, default = datetime.utcnow())
    last_seen = db.Column(db.DateTime, default = datetime.utcnow())
    full_name = db.Column(db.String(128))
    show_personal = db.Column(db.Integer)
    admin = db.Column(db.Integer)
    author = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    followed = db.relationship(
        'Users', secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = db.backref('followers', lazy = 'dynamic'),
        lazy = 'dynamic'
    )

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
       digest = md5(self.email.lower().encode('utf-8')).hexdigest()
       return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Posts.query.join(followers, (followers.c.followed_id == Posts.users_id)).filter(followers.c.follower_id == self.id).filter(Posts.published == "1").order_by(Posts.timestamp.desc())

    def followed_and_their_posts(self):
        followed = Posts.query.join(followers, (followers.c.followed_id == Posts.users_id)).filter(followers.c.follower_id == self.id)
        own = Posts.query.filter_by(users_id = self.id)
        return followed.union(own).order_by(Posts.timestamp.desc())

    def get_reset_password_token(self, expires_in = 600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')

    def generate_confirmation_token(self, expires_in = 600):
        return jwt.encode({'confirm_email': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return Users.query.get(id)

    @staticmethod
    def verify_confirmation_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['confirm_email']
        except:
            return
        return Users.query.get(id)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))



posttag = db.Table('posttag',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    )

@whooshee.register_model('title', 'content')
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128))
    slug = db.Column(db.String(128), unique = True)
    content = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, default = datetime.utcnow())
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    published = db.Column(db.Integer)
    language = db.Column(db.String(5))

    assignedtags = db.relationship('Tags', secondary = posttag, backref = db.backref('posts', lazy = 'dynamic'), lazy='dynamic')


    def __init__(self, *args, **kwargs):
        super(Posts, self).__init__(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)


    def __repr__(self):
        return '<Post: {}>'.format(self.title)


    def assign_tag(self, tag):
        if not self.is_assigned_tag(tag):
            self.assignedtags.append(tag)

    def unassign_tag(self, tag):
        if self.is_assigned_tag(tag):
            self.assignedtags.remove(tag)

    def is_assigned_tag(self, tag):
        return self.assignedtags.filter(posttag.c.tag_id == tag.id).count() > 0



class Categorys(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    slug = db.Column(db.String(64), unique = True)
    posts = db.relationship('Posts', backref = 'category', lazy = 'dynamic')

    def __init__(self, *args, **kwargs):
        super(Categorys, self).__init__(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)

    def __repr__(self):
        return '<Category: {}>'.format(self.name)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    slug = db.Column(db.String(64), unique = True)

    def __init__(self, *args, **kwargs):
        super(Tags, self).__init__(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)
