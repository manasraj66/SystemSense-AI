from flask import Blueprint, jsonify, current_app
from app.models import SystemMetric
from app.services.collector_service import collect_snapshot
from app.services.storage_service import save_metric
from app.services.anomaly_service import detect_latest
bp = Blueprint("metrics", __name__, url_prefix="/api")
@bp.get("/metrics")
def metrics():
    rows = SystemMetric.query.order_by(SystemMetric.timestamp.desc()).limit(60).all()[::-1]
    return jsonify([r.to_dict() for r in rows])
@bp.get("/metrics/latest")
def latest():
    row = SystemMetric.query.order_by(SystemMetric.id.desc()).first()
    return jsonify(row.to_dict() if row else {})
@bp.post("/metrics/collect")
def collect():
    row = save_metric(collect_snapshot())
    detect_latest(row, current_app.config)
    return jsonify(row.to_dict()), 201
