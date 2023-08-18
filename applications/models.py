from datetime import datetime
from hashlib import md5
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from applications.database import db
from flask import current_app as app

followers = db.Table(
    'followers',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), unique=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), unique=True)
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    about_me = db.Column(db.String(140), default="")
    imgProfile = db.Column(db.String(300))
    posts = db.relationship('Post', backref='author', lazy='dynamic', passive_deletes=True)
    posts_liked = db.relationship('Likes', backref='user', lazy='dynamic', passive_deletes=True)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic', passive_deletes=True)
    comment = db.relationship('Comments', backref='author', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return '<User: %s>' % self.username

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
        followed = Post.query.join(followers, (followers.c.followed_id == Post.id)).filter(
            followers.c.followed_id == self.id)
        own = Post.query.filter_by(user_id=self.id).order_by(Post.timestamp.desc()).limit(1)
        return followed.union(own).order_by(Post.timestamp.desc())

    def like_post(self, post):
        if not self.post_liked(post):
            like = Likes(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def dislike_post(self, post):
        if self.post_liked(post):
            Likes.query.filter_by(user_id=self.id, post_id=post.id).delete()

    def post_liked(self, post):
        return Likes.query.filter(Likes.user_id == self.id, Likes.post_id == post.id).count() > 0

    def following(self):
        return User.query.filter((followers.c.follower_id == User.id)).filter(
            followers.c.followed_id == self.id)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    img = db.Column(db.String(300))
    description = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
    likes = db.relationship('Likes', backref='likes', lazy='dynamic', passive_deletes=True)
    comments = db.relationship('Comments', backref='comments', lazy='dynamic', passive_deletes=True)
    count_likes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post {}>'.format(self.img)


class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Likes {}>'.format(self.id)


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
