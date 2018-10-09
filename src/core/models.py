from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# Shared db module for todo and user models.
db = SQLAlchemy()

class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
