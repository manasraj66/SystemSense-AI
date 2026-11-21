from flask import Blueprint, jsonify
from app.services.process_service import get_process_table
bp = Blueprint("processes", __name__, url_prefix="/api")
@bp.get("/processes")
def processes(): return jsonify(get_process_table())
