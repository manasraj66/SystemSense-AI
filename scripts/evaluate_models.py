import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.models import SystemMetric
from app.ml.regression.random_forest_regressor import train
from app.ml.evaluator import regression_metrics
app=create_app()
with app.app_context():
    values=[r.cpu_percent for r in SystemMetric.query.order_by(SystemMetric.timestamp.asc()).all()]
    if len(values)<10: raise SystemExit("Collect at least 10 samples first.")
    split=int(len(values)*.8)
    if split<2 or split==len(values): raise SystemExit("Not enough records for an 80/20 split.")
    model=train(values[:split])
    pred=model.predict([[i] for i in range(split,len(values))])
    print(regression_metrics(values[split:],pred))
