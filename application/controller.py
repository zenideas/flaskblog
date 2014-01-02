from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from application import app, db, lm, oid
from forms import LoginForm, UserForm, PostForm, SearchForm
from models import User, ROLE_USER, ROLE_ADMIN, Post
from datetime import datetime
from emails import follower_notification


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

    g.search_form = SearchForm()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET','POST'])
@login_required
def index(page=1):
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is live fro now')
        redirect(url_for('index'))
    posts = g.user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html',
        title = 'Home',
        form = form,
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
@app.route('/user/<email>/<int:page>')
@login_required
def user(email, page=1):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash("User " + email + "not exists")
        redirect('index')
    posts = user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['POST', 'GET'])
@login_required
# Validate Unique Nickname
def edit():
    form = UserForm(g.user.nickname)
    if request.method == 'POST' and form.validate_on_submit():
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


@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        redirect(url_for('index'))
    return redirect(url_for('search_result', q=g.search_form.search.data))


@app.route('/search_result/<q>', methods=['GET'])
@login_required
def search_result(q):
    results = Post.query.whoosh_search(q, app.config['MAX_SEARCH_RESULTS']).all()
    return render_template('search_result.html', q=q, results=results)


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
        # Fixed Unique Problem
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
        # Make self follow
        db.session.add(user.follow(user))
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


@app.route('/follow/<email>')
@login_required
def do_follow(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User Doesn\'t exists ')
        return redirect(url_for('index'))

    if user == g.user:
        flash('You cannot follow your-self')
        return redirect(url_for('user', email=email))
    u = g.user.follow(user)
    if u is None:
        flash('cannot follow ' + user.nickname)
        return redirect(url_for('user', nickname = user.nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + u.nickname)
    follower_notification(user, g.user)
    return redirect(url_for(nickname=u.nickname))

@app.route('/unfollow/<email>')
@login_required
def do_unfollow(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User Doesn\'t exists ')
        return redirect(url_for('index'))

    if user == g.user:
        flash('You cannot follow or unfollow your-self')
        return redirect(url_for('user', email=email))
    u = g.user.unfollow(user)
    if u is None:
        flash('cannot unfollow ' + user.nickname)
        return redirect(url_for('user', nickname = user.nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now unfollowing ' + u.nickname)
    return redirect(url_for(nickname=u.nickname))


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
