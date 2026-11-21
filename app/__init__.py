from pathlib import Path
from flask import Flask
from config import Config
from .extensions import db, socketio

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if db_uri.startswith("sqlite:///"):
        Path(db_uri.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)
    for folder in (app.config["MODEL_DIR"], app.config["REPORT_DIR"], app.config["DATA_DIR"], app.config["LOG_DIR"]):
        Path(folder).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode="threading")
    from .routes import register_blueprints
    register_blueprints(app)
    with app.app_context():
        db.create_all()
    if not app.config.get("TESTING"):
        from scheduler.jobs import register_jobs
        register_jobs(app)
    return app
