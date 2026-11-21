from app.models import SystemMetric
from app.ml.anomaly.isolation_forest import train as train_anomaly
from app.ml.regression.random_forest_regressor import train as train_regression
from app.ml.model_registry import save_model
def train_all():
    rows = SystemMetric.query.order_by(SystemMetric.timestamp.asc()).all()
    if len(rows) < 20:
        return {"trained": False, "reason": "Collect at least 20 samples first."}
    save_model(train_anomaly(rows), "isolation_forest.joblib")
    save_model(train_regression([r.cpu_percent for r in rows]), "random_forest_regressor.joblib")
    return {"trained": True, "samples": len(rows)}
