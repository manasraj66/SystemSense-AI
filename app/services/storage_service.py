from app.extensions import db
from app.models import ProcessSnapshot
def save_metric(row):
    db.session.add(row)
    db.session.commit()
    return row
def save_processes(items):
    for p in items:
        db.session.add(ProcessSnapshot(pid=p["pid"], name=p["name"], username=p["username"],
            cpu_percent=p["cpu_percent"], memory_percent=p["memory_percent"], status=p["status"]))
    db.session.commit()
