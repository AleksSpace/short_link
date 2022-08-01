import re

from . import constants


def len_validation(string, exception):
    try:
        getattr(string, '__len__')
    except AttributeError:
        raise AttributeError
    if constants.MIN_LEN_SHORT_URL <= len(string) <= constants.MAX_LEN_SHORT_URL:
        return
    raise exception


def regex_validation(string, exception):
    if re.match(constants.PATTERN, string):
        return
    raise exception
