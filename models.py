from microblog import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    scheduled_time = db.Column(db.String, nullable=False)
    should_alert = db.Column(db.Boolean, default=True, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=True)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    def __init__(self, title, scheduled_time, should_alert):
        self.title = title
        self.scheduled_time = scheduled_time
        self.should_alert = should_alert
