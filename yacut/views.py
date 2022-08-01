from datetime import datetime
# from pprint import pprint

from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user

from . import app, constants, db
from .forms import LinkForm, LoginForm, RegForm
from .models import URL_map, User
from .utils import check_short_url, get_unique_short_id
from yacut import login_manager


@app.route('/', methods=['GET', 'POST'])
@login_required
def index_view():
    form = LinkForm()
    if not form.validate_on_submit():
        return render_template('main_page.html', form=form)
    original = form.original_link.data
    short = form.custom_id.data
    timestop = form.time_live.data
    if short:
        if check_short_url(short):
            flash(constants.NAME_BUSY.format(short))
            return render_template('main_page.html', form=form)
    else:
        short = get_unique_short_id(constants.LEN_SHORT_URL)
    url_link = URL_map(
        original=original,
        short=short,
        timestop=timestop,
    )
    db.session.add(url_link)
    db.session.commit()
    flash(constants.URL_READY)
    flash(short)
    return render_template('main_page.html', form=form)


@app.route('/<string:short_url>')
def redirect_to_url(short_url):
    time_stop = URL_map.query.all()
    time_timestop = time_stop[-1].timestop
    time_now = datetime.now()
    if time_timestop > time_now:
        original_url = URL_map.query.filter_by(short=short_url).first_or_404()
        return redirect(original_url.original)
    return render_template('time_and.html')


@app.route('/registration/', methods=['post', 'get'])
def registration():
    form = RegForm()
    if not form.validate_on_submit():
        return render_template('registration.html', form=form)
    name = form.name.data
    username = form.username.data
    email = form.email.data
    password = form.password.data
    ip_user = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user_save = User(name=name,
                     username=username,
                     email=email,
                     ip_user=ip_user)
    user_save.set_password(password)
    db.session.add(user_save)
    db.session.commit()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_view'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index_view'))

        flash("Invalid username/password", 'error')
        return redirect(url_for('index_view'))
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
