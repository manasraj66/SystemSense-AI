import psutil
from app.models import SystemMetric

def collect_snapshot():
    cpu = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory().percent
    disk_path = "C:\\" if psutil.WINDOWS else "/"
    disk = psutil.disk_usage(disk_path).percent
    net = psutil.net_io_counters()
    return SystemMetric(cpu_percent=cpu, memory_percent=memory, disk_percent=disk,
        network_sent_mb=round(net.bytes_sent/1024**2, 2),
        network_recv_mb=round(net.bytes_recv/1024**2, 2), process_count=len(psutil.pids()))

def list_processes(limit=100):
    result = []
    for proc in psutil.process_iter(["pid", "name", "username", "status", "memory_percent"]):
        try:
            p = proc.info
            result.append({"pid": p["pid"], "name": p.get("name") or "Unknown",
                "username": p.get("username") or "N/A", "status": p.get("status") or "unknown",
                "memory_percent": round(p.get("memory_percent") or 0, 2),
                "cpu_percent": round(proc.cpu_percent(interval=None), 2)})
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return sorted(result, key=lambda x: x["cpu_percent"], reverse=True)[:limit]
