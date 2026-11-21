import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.models import SystemMetric
from app.ml.anomaly.isolation_forest import train
from app.ml.model_registry import save_model
app=create_app()
with app.app_context():
    rows=SystemMetric.query.order_by(SystemMetric.timestamp.asc()).all()
    if len(rows)<20: raise SystemExit("Collect at least 20 samples first.")
    save_model(train(rows),"isolation_forest.joblib")
    print(f"Trained using {len(rows)} records.")
