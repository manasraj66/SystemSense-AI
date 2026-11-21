from datetime import datetime, timezone
from app.extensions import db
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    severity = db.Column(db.String(20), default="warning")
    acknowledged = db.Column(db.Boolean, default=False)
