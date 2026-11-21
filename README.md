# SystemSense AI — Intelligent System Monitoring & Predictive Analytics

A full-stack Flask major-project starter that monitors the host computer, stores telemetry,
flags unusual resource usage, forecasts CPU load, explores processes, and exports reports.

## Features
- CPU, RAM, disk, network counters and process count using psutil.
- Responsive dark dashboard with Chart.js and periodic data refresh.
- SQLite models for metrics, anomalies, predictions, alerts and process snapshots.
- Rule-based alerts plus Isolation Forest anomaly detection when sufficient history exists.
- CPU forecasting with Random Forest after enough samples and a moving-average fallback.
- Process explorer, metric history, anomaly page, alerts and CSV/PDF reports.
- APScheduler background collection and retention cleanup.
- REST endpoints and pytest tests.

## Windows PowerShell setup
```powershell
cd systemsense-ai
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/init_db.py
python run.py
```
Open http://127.0.0.1:5000

## Important
The app monitors the computer running the Flask server. It does not terminate processes.
Predictions are estimates and improve as you collect more data. Before public deployment,
configure a strong SECRET_KEY, authentication, HTTPS, authorization and protected exports.
