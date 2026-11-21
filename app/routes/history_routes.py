from flask import Blueprint, jsonify, request
from app.models import SystemMetric
bp = Blueprint("history", __name__, url_prefix="/api")
@bp.get("/history")
def history():
    limit = max(1,min(int(request.args.get("limit",200)),2000))
    rows = SystemMetric.query.order_by(SystemMetric.timestamp.desc()).limit(limit).all()[::-1]
    return jsonify([r.to_dict() for r in rows])
