from datetime import datetime

from flask import flash, redirect, render_template

from . import app, constants, db
from .forms import LinkForm
from .models import URL_map
from .utils import check_short_url, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
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
