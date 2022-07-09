from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

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
    submit = SubmitField('Преобразовать')
