from datetime import datetime, timezone
from app.extensions import db
class AnomalyRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    metric_name = db.Column(db.String(40), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    score = db.Column(db.Float)
    severity = db.Column(db.String(20), default="medium")
    description = db.Column(db.String(255), nullable=False)
