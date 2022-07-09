from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, constants, db
from .forms import LinkForm
from .models import URL_map
from .utils import check_short_url, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if short:
            if check_short_url(short):
                flash(constants.NAME_BUSY.format(short))
                return render_template('main_page.html', form=form)
        else:
            short = get_unique_short_id(6)
        url_link = URL_map(
            original=original,
            short=short
        )
        db.session.add(url_link)
        db.session.commit()
        flash(constants.URL_READY)
        flash(short)
    return render_template('main_page.html', form=form)


@app.route('/<string:short_url>')
def redirect_to_url(short_url):
    original_url = URL_map.query.filter_by(short=short_url).first()
    if original_url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(original_url.original)
