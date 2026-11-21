from datetime import datetime, timezone
from app.extensions import db
class ProcessSnapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    pid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))
    username = db.Column(db.String(120))
    cpu_percent = db.Column(db.Float, default=0)
    memory_percent = db.Column(db.Float, default=0)
    status = db.Column(db.String(40))
