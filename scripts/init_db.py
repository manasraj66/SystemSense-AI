import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.extensions import db
app=create_app({"TESTING":True})
with app.app_context():
    db.create_all()
    print("SystemSense AI database initialized.")
