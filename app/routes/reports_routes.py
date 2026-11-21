from flask import Blueprint, current_app, send_file
from app.services.report_service import export_csv, export_pdf
bp = Blueprint("reports", __name__, url_prefix="/api/reports")
@bp.get("/csv")
def csv_report(): return send_file(export_csv(current_app.config["REPORT_DIR"]), as_attachment=True)
@bp.get("/pdf")
def pdf_report(): return send_file(export_pdf(current_app.config["REPORT_DIR"]), as_attachment=True)
