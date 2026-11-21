import numpy as np
from app.extensions import db
from app.models import SystemMetric, AnomalyRecord
from app.services.alert_service import create_alert

def detect_latest(metric, config):
    found = []
    for name, value, threshold in [
        ("CPU", metric.cpu_percent, config["CPU_WARNING"]),
        ("Memory", metric.memory_percent, config["MEMORY_WARNING"]),
        ("Disk", metric.disk_percent, config["DISK_WARNING"])
    ]:
        if value >= threshold:
            severity = "critical" if value >= min(99, threshold + 10) else "warning"
            message = f"{name} usage reached {value:.1f}% (threshold {threshold:.1f}%)."
            row = AnomalyRecord(metric_name=name.lower(), metric_value=value,
                severity=severity, description=message)
            db.session.add(row)
            create_alert(f"{name} usage is high", message, severity)
            found.append(row)
    history = SystemMetric.query.order_by(SystemMetric.id.desc()).limit(200).all()
    if len(history) >= 40:
        try:
            from sklearn.ensemble import IsolationForest
            x = np.array([[r.cpu_percent, r.memory_percent, r.disk_percent] for r in history])
            detector = IsolationForest(contamination=0.05, random_state=42).fit(x)
            if detector.predict(x[:1])[0] == -1 and not found:
                row = AnomalyRecord(metric_name="combined", metric_value=metric.cpu_percent,
                    score=float(detector.decision_function(x[:1])[0]), severity="medium",
                    description="Isolation Forest identified an unusual combined resource pattern.")
                db.session.add(row)
                found.append(row)
        except Exception:
            pass
    db.session.commit()
    return found
