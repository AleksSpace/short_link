from datetime import datetime

import pytz
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from short_link import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text(), nullable=False, index=True)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.now(pytz.timezone("Europe/Moscow")))
    timestop = db.Column(db.DateTime,
                         index=True)

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(),
                           default=datetime.now(pytz.timezone("Europe/Moscow")))
    updated_on = db.Column(db.DateTime(),
                           default=datetime.now(pytz.timezone("Europe/Moscow")),
                           onupdate=datetime.now(pytz.timezone("Europe/Moscow")))
    ip_user = db.Column(db.String(15))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
