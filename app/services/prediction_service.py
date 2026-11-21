import numpy as np
from app.extensions import db
from app.models import SystemMetric, PredictionLog

def predict_cpu(horizon=5):
    rows = SystemMetric.query.order_by(SystemMetric.id.desc()).limit(300).all()[::-1]
    values = np.array([r.cpu_percent for r in rows], dtype=float)
    prediction = float(np.mean(values[-5:])) if len(values) else 0.0
    model_name = "Moving-average baseline"
    if len(values) >= 30:
        try:
            from sklearn.ensemble import RandomForestRegressor
            x = np.arange(len(values)).reshape(-1, 1)
            model = RandomForestRegressor(n_estimators=100, random_state=42).fit(x, values)
            prediction = float(model.predict([[len(values) + horizon]])[0])
            model_name = "Random Forest Regressor"
        except Exception:
            pass
    row = PredictionLog(horizon_minutes=horizon,
        predicted_value=round(float(np.clip(prediction, 0, 100)), 2), model_name=model_name)
    db.session.add(row)
    db.session.commit()
    return row
