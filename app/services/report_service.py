import csv
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.models import SystemMetric, AnomalyRecord

def export_csv(folder):
    path = Path(folder)/f"systemsense_metrics_{datetime.now():%Y%m%d_%H%M%S}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu_percent", "memory_percent", "disk_percent", "process_count"])
        for r in SystemMetric.query.order_by(SystemMetric.timestamp.asc()).all():
            writer.writerow([r.timestamp.isoformat(), r.cpu_percent, r.memory_percent, r.disk_percent, r.process_count])
    return path

def export_pdf(folder):
    path = Path(folder)/f"systemsense_report_{datetime.now():%Y%m%d_%H%M%S}.pdf"
    c = canvas.Canvas(str(path), pagesize=A4)
    _, height = A4
    y = height-55
    c.setFont("Helvetica-Bold", 17)
    c.drawString(42, y, "SystemSense AI - System Health Report")
    y -= 25
    c.setFont("Helvetica", 9)
    c.drawString(42, y, f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}")
    y -= 30
    for r in SystemMetric.query.order_by(SystemMetric.timestamp.desc()).limit(25).all():
        c.drawString(42, y, f"{r.timestamp:%Y-%m-%d %H:%M:%S} | CPU {r.cpu_percent:.1f}% | RAM {r.memory_percent:.1f}% | Disk {r.disk_percent:.1f}%")
        y -= 15
        if y < 55:
            c.showPage()
            y = height-50
            c.setFont("Helvetica", 9)
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(42, y, "Recent anomaly events")
    y -= 20
    c.setFont("Helvetica", 9)
    for a in AnomalyRecord.query.order_by(AnomalyRecord.timestamp.desc()).limit(10).all():
        c.drawString(42, y, f"{a.metric_name}: {a.description[:105]}")
        y -= 15
        if y < 55:
            c.showPage()
            y = height-50
            c.setFont("Helvetica", 9)
    c.save()
    return path
