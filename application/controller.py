from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from application import app, db, lm, oid
from forms import LoginForm, UserForm
from models import User, ROLE_USER, ROLE_ADMIN
from datetime import datetime


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {'author':{ 'nickname': 'John' }, 'body': 'Beautiful day in Portland!'},
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
        title = 'Home',
        user = user,
        posts = posts)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',title='Sign In', form = form, providers=app.config['OPENID_PROVIDERS'])


@app.route('/user/<email>')
@login_required
def user(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash("User " + email + "not exists")
        redirect('index')
    posts = [{"author" : user, "body" : "Test Post #1"},{"author" : user, "body" : "Test Post #2"}]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['POST', 'GET'])
@login_required
def edit():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit:
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('your changed has been saved')
        redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edituser.html', form=form, user=g.user)


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
