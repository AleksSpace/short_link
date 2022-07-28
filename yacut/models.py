from datetime import datetime

import pytz

from yacut import db


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
