from random import choices

from .constants import SYMBOLS
from .models import URL_map


def get_unique_short_id(num):
    while True:
        short_link = ''.join(choices(SYMBOLS, k=num))
        if not URL_map.query.filter_by(short=short_link).first():
            break
    return short_link


def check_short_url(short_url):
    return bool(URL_map.query.filter_by(short=short_url).first())
