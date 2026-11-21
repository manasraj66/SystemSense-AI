import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.services.collector_service import collect_snapshot
from app.services.storage_service import save_metric
app=create_app({"TESTING":True})
with app.app_context():
    print(save_metric(collect_snapshot()).to_dict())
