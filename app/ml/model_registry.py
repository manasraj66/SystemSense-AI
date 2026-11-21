import joblib
from pathlib import Path
from flask import current_app
def save_model(model, filename):
    path = Path(current_app.config["MODEL_DIR"])/filename
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return path
def load_model(filename):
    path = Path(current_app.config["MODEL_DIR"])/filename
    return joblib.load(path) if path.exists() else None
