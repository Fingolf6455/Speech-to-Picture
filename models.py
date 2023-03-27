from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_url = db.Column(db.String, nullable=True)
    thumbnail_url = db.Column(db.String, nullable=True)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_posted': self.date_posted.isoformat(),
            'image_url': self.image_url,
            'thumbnail_url': self.thumbnail_url
        }
    def __repr__(self):
        return f"Recording('{self.title}', '{self.date_posted}', '{self.image_url}', '{self.thumbnail_url}')"
