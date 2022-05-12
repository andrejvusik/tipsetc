from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from blog import db, login, whooshee


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

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
       digest = md5(self.email.lower().encode('utf-8')).hexdigest()
       return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, users):
        if not self.is_following(users):
            self.followed.append(users)

    def unfollow(self, users):
        if self.is_following(users):
            self.followed.remove(users)

    def is_following(self, users):
        return self.followed.filter(followers.c.followed_id == users.id).count() > 0

    def followed_posts(self):
        return Posts.query.join(
            followers, (followers.c.followed_id == Posts.users_id)).filter(
                followers.c.follower_id == self.id).filter(Posts.published == "1").order_by(Posts.timestamp.desc())

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


@whooshee.register_model('title', 'content')
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128))
    slug = db.Column(db.String(128), unique = True)
    content = db.Column(db.Text())
    category = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default = datetime.utcnow())
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    published = db.Column(db.Integer)
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.title)
