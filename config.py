import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-before-deployment")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'database' / 'systemsense.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COLLECT_INTERVAL_SECONDS = int(os.getenv("COLLECT_INTERVAL_SECONDS", "5"))
    CPU_WARNING = float(os.getenv("CPU_WARNING", "80"))
    MEMORY_WARNING = float(os.getenv("MEMORY_WARNING", "85"))
    DISK_WARNING = float(os.getenv("DISK_WARNING", "90"))
    HISTORY_RETENTION_DAYS = int(os.getenv("HISTORY_RETENTION_DAYS", "30"))
    MODEL_DIR, REPORT_DIR, DATA_DIR, LOG_DIR = ROOT/"ml_models", ROOT/"reports", ROOT/"data", ROOT/"logs"
