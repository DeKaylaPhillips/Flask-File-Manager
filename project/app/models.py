from app import db
from datetime import datetime


class Files(db.Model):
    __tablename__ = 'File'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False, index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    extension = db.Column(db.String(5))
    path = db.Column(db.String, unique=True)
    headers = db.Column(db.String)
