from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, constants, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id
from .validators import len_validation, regex_validation


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(constants.EMPTY_REQUEST, HTTPStatus.BAD_REQUEST)
    original = data.get('url')
    if original is None:
        raise InvalidAPIUsage(constants.REQ_FIELD)
    short = data.get('custom_id')
    if short:
        len_validation(short, InvalidAPIUsage(constants.BAD_NAMING))
        regex_validation(short, InvalidAPIUsage(constants.BAD_NAMING))
        if URL_map.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage(constants.API_NAME_BUSY.format(short))
    else:
        short = get_unique_short_id(6)
    url_link = URL_map(
        original=original,
        short=short
    )
    db.session.add(url_link)
    db.session.commit()
    response_dict = {
        'url': original,
        'short_link': url_for(
            'redirect_to_url', short_url=short, _external=True
        ),
    }
    return jsonify(response_dict), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_full_url_link(short_id):
    short = URL_map.query.filter_by(short=short_id).first()
    if short is None:
        raise InvalidAPIUsage(constants.NO_ID, HTTPStatus.NOT_FOUND)
    return dict(url=f'{short.original}'), HTTPStatus.OK
