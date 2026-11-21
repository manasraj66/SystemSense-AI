from flask import Blueprint, jsonify
from app.models import AnomalyRecord
bp = Blueprint("analyze", __name__, url_prefix="/api")
@bp.get("/anomalies")
def anomalies():
    rows = AnomalyRecord.query.order_by(AnomalyRecord.timestamp.desc()).limit(100).all()
    return jsonify([{"id":r.id,"timestamp":r.timestamp.isoformat(),"metric":r.metric_name,
        "value":r.metric_value,"severity":r.severity,"description":r.description} for r in rows])
