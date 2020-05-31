from app import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), index=True, unique=False)
    message = db.Column(db.JSON(), index=False, unique=False)
