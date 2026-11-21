from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from app.extensions import socketio, db
from app.services.collector_service import collect_snapshot, list_processes
from app.services.storage_service import save_metric, save_processes
from app.services.anomaly_service import detect_latest

scheduler = BackgroundScheduler(daemon=True)

def collect_job(app):
    with app.app_context():
        row = save_metric(collect_snapshot())
        detect_latest(row, app.config)
        save_processes(list_processes(25))
        socketio.emit("metric_update", row.to_dict())

def cleanup_job(app):
    from app.models import SystemMetric, ProcessSnapshot
    with app.app_context():
        cutoff = datetime.now(timezone.utc)-timedelta(days=app.config["HISTORY_RETENTION_DAYS"])
        SystemMetric.query.filter(SystemMetric.timestamp < cutoff).delete()
        ProcessSnapshot.query.filter(ProcessSnapshot.timestamp < cutoff).delete()
        db.session.commit()

def register_jobs(app):
    if scheduler.running: return
    scheduler.add_job(collect_job,"interval",seconds=app.config["COLLECT_INTERVAL_SECONDS"],
        args=[app],id="collector",replace_existing=True,max_instances=1)
    scheduler.add_job(cleanup_job,"interval",hours=24,args=[app],id="cleanup",replace_existing=True)
    scheduler.start()
