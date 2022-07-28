from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from . import constants


class LinkForm(FlaskForm):
    original_link = URLField(
        'Добавьте вашу ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Некорректный URL')]
    )
    custom_id = StringField(
        'Введите ваш вариант ссылки',
        validators=[Optional(),
                    Length(constants.MIN_LEN_SHORT_URL,
                           constants.MAX_LEN_SHORT_URL,
                           message='Максимальная длина ссылки: 16 символов'),
                    Regexp(constants.PATTERN,
                           message='Допускается только латиница и арабские цифры.')]
    )
    time_live = DateTimeField(
        'Введите время жизни ссылки',
        format=constants.FORMAT_DATE,
        validators=[Optional()]
    )
    submit = SubmitField('Преобразовать')

    def validate_time_live(self, time_live):
        time_from_form = time_live.data
        try:
            time_from_form_str = time_from_form.strftime(constants.FORMAT_DATE)
            datetime.strptime(time_from_form_str, constants.FORMAT_DATE)
        except Exception:
            raise ValidationError(constants.NO_FORMAT_DATE)
        if time_from_form < datetime.now():
            raise ValidationError(constants.NO_DATETIME_PAST)
