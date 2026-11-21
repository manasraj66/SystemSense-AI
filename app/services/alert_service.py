from app.extensions import db
from app.models import Alert
def create_alert(title, message, severity="warning"):
    row = Alert(title=title, message=message, severity=severity)
    db.session.add(row)
    db.session.commit()
    return row
