from datetime import datetime, timezone
from app.extensions import db
class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    metric_name = db.Column(db.String(40), default="cpu_percent")
    horizon_minutes = db.Column(db.Integer, default=5)
    predicted_value = db.Column(db.Float, nullable=False)
    model_name = db.Column(db.String(80), default="baseline")
