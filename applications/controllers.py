import os
import sqlite3

from flask import render_template, url_for, redirect, session, current_app, request, flash, jsonify, g
from flask import current_app as app
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from sqlalchemy import values
from werkzeug.utils import secure_filename
from app import photos
from applications.forms import *
from applications.models import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return redirect(url_for('signin'))


@app.route('/login', methods=['GET', 'POST'])
def signin():  # put application's code here
    form = signinForm()
    logo = os.path.join('static/images/','blog1.png')
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                # user.last_login = str(datetime.today())[:16]
                login_user(user)
                return redirect(url_for('explore'))
    return render_template('signin.html', form=form,icon=logo)


@app.route('/signup', methods=['GET', 'POST'])
def signup():  # put application's code here
    form = signupForm()
    logo = os.path.join('static/images/','blog1.png')
    if form.validate_on_submit():
        new_user = User(username=form.username.data, f_name=form.f_name.data, l_name=form.l_name.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form,icon=logo)


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):  # put application's code here'
    user = User.query.filter_by(username=username).first_or_404()
    if user is None:
        user = User.query.filter_by(id=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.timestamp.desc()).all()
    count = len(posts)
    return render_template("profile.html", username=username, user=user, posts=posts, count=count)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():  # put application's code here'
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('signin'))


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        filename = photos.save(form.img.data)
        url = photos.url(filename)
        ui = url.replace('_uploads', 'static')
        post = Post(img=ui, author=current_user, description=form.desc.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username))
    return render_template('post.html', form=form)


@app.route('/p/<id>')
@login_required
def post_detail(id):
    post = Post.query.filter_by(id=id).first_or_404()
    comments = Comments.query.filter_by().all()
    user = current_user
    return render_template('post_detail.html', post=post, user=user, comments=comments)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = Searchform(request.form)
    if request.method == 'POST':
        text = form.search.data
        return redirect(url_for('sresults', search=text))
    return render_template('search.html', form=form)


@app.route('/results/<search>', methods=['GET', 'POST'])
@login_required
def sresults(search):
    results = db.session.query(User).filter(User.username.like('%' + search + '%'))
    return render_template('results.html', results=results)


@app.route('/profile/<username>/edit', methods=['POST', 'GET'])
@login_required
def edit_profile(username):
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('profile', username=username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@app.route('/p/<id>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    form = EditPostForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        filename = photos.save(form.img.data)
        url = photos.url(filename)
        ui = url.replace('_uploads', 'static')
        post.img = ui
        post.description = form.desc.data
        db.session.commit()
        return render_template('edit_post.html', form=form)
    elif request.method == 'GET':
        # form.img.data = post.img
        form.desc.data = post.description
    return render_template('edit_post.html', form=form)


@app.route('/explore')
@login_required
def explore():
    global posts
    posts = list()

    posts = Post.query.filter_by().all()
    return render_template('explore.html', posts=posts)


@app.route('/feed')
@login_required
def feed():
    global posts
    posts = list()

    posts = Post.query.filter(Post.user_id == followers.c.followed_id).all()
    return render_template('explore.html', posts=posts)


@app.route('/follow/<username>')
@login_required
def follow(username):
    followers_cnt = followers.insert().values(follower_id=current_user.id, followed_id=username)
    db.session.execute(followers_cnt)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(user.username))
    return redirect(url_for('profile', username=username, user=user))


@app.route('/<username>/followings', methods=['GET', 'POST'])
@login_required
def all_followings(username):
    user = User.query.filter(User.username == username).first_or_404()
    # print(user)
    return render_template('following.html', users=user.followed)


@app.route('/<username>/followers', methods=['GET', 'POST'])
@login_required
def all_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('followers.html', users=user.following())


@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
        flash('Post Liked')
    if action == 'dislike':
        current_user.dislike_post(post)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/delete_post/<id>')
@login_required
def delete_post(id):
    Comments.query.filter_by(post_id=int(id)).delete()
    Post.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect('/profile/{}'.format(current_user.username))


@app.route('/addComment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def addComment(post_id):
    body = request.form['Comment']
    new_comment = Comments(user_id=current_user.id, post_id=int(post_id), body=body)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(request.referrer)
