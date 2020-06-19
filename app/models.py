import datetime

from app import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), index=True, unique=False, nullable=False)
    channel = db.Column(db.String(), index=False, unique=False, nullable=True)
    ts = db.Column(db.String(), index=False, unique=False, nullable=True)
    created = db.Column(db.DateTime(), index=True, nullable=False, default=datetime.datetime.now)
