from datetime import datetime, timezone
from app.extensions import db
class SystemMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    cpu_percent = db.Column(db.Float, nullable=False)
    memory_percent = db.Column(db.Float, nullable=False)
    disk_percent = db.Column(db.Float, nullable=False)
    network_sent_mb = db.Column(db.Float, default=0)
    network_recv_mb = db.Column(db.Float, default=0)
    process_count = db.Column(db.Integer, default=0)
    def to_dict(self):
        return {"id": self.id, "timestamp": self.timestamp.isoformat(), "cpu": self.cpu_percent,
                "memory": self.memory_percent, "disk": self.disk_percent,
                "network_sent_mb": self.network_sent_mb, "network_recv_mb": self.network_recv_mb,
                "process_count": self.process_count}
