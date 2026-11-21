from flask import Blueprint, jsonify, request
from app.services.prediction_service import predict_cpu
from app.models import PredictionLog
bp = Blueprint("predict", __name__, url_prefix="/api")
@bp.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    horizon = max(1, min(int(payload.get("horizon",5)),60))
    row = predict_cpu(horizon)
    return jsonify({"prediction":row.predicted_value,"metric":row.metric_name,
        "horizon_minutes":row.horizon_minutes,"model":row.model_name})
@bp.get("/predictions")
def predictions():
    rows = PredictionLog.query.order_by(PredictionLog.created_at.desc()).limit(50).all()
    return jsonify([{"created_at":r.created_at.isoformat(),"value":r.predicted_value,
        "horizon":r.horizon_minutes,"model":r.model_name} for r in rows])
