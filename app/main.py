from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import analyze_query, analyze_logs_by_file, get_logs_summary
from app.fetch_logs import fetch_and_save_all_logs
from app.continuous_monitor import start_monitoring, stop_monitoring, get_scheduler_status

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio

# ✅ FIRST create app
app = FastAPI()

# ✅ THEN mount static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Request models
class QueryRequest(BaseModel):
    query: str

class FetchLogsRequest(BaseModel):
    hours: int = 24
    grafana_api_key: str = None

class MonitoringRequest(BaseModel):
    interval_minutes: int = 15
    grafana_api_key: str = None

# UI route
@app.get("/")
def home():
    return FileResponse("app/static/index.html")

# API route for analysis
@app.post("/analyze")
def analyze(request: QueryRequest):
    result = analyze_query(request.query)
    return {"response": result}

# API route for per-file analysis
@app.post("/analyze-files")
def analyze_files(request: QueryRequest = None):
    """Analyze logs from each file separately"""
    try:
        query = request.query if request else None
        reports = analyze_logs_by_file(query)
        return {
            "status": "success",
            "reports": reports
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# API route to get logs summary
@app.get("/logs-summary")
def logs_summary():
    """Get summary statistics for each log file"""
    try:
        summary = get_logs_summary()
        return {
            "status": "success",
            "summary": summary
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# API route to fetch logs from Loki, Prometheus, Grafana
@app.post("/fetch-logs")
async def fetch_logs_endpoint(request: FetchLogsRequest = None):
    """
    Fetch logs from all sources (Loki, Prometheus, Grafana)
    and save to data folder
    """
    try:
        hours = request.hours if request else 24
        grafana_api_key = request.grafana_api_key if request else None
        
        await asyncio.to_thread(
            fetch_and_save_all_logs,
            hours=hours,
            grafana_api_key=grafana_api_key
        )
        
        return {
            "status": "success",
            "message": "Logs fetched from Loki, Prometheus, and Grafana",
            "files": [
                "data/loki.log",
                "data/prometheus.log",
                "data/grafana.log"
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# API route to start continuous monitoring
@app.post("/monitoring/start")
def start_monitoring_endpoint(request: MonitoringRequest = None):
    """Start continuous log monitoring"""
    try:
        interval = request.interval_minutes if request else 15
        grafana_api_key = request.grafana_api_key if request else None
        
        start_monitoring(
            interval_minutes=interval,
            grafana_api_key=grafana_api_key
        )
        
        return {
            "status": "success",
            "message": f"Monitoring started - fetching logs every {interval} minutes"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# API route to stop continuous monitoring
@app.post("/monitoring/stop")
def stop_monitoring_endpoint():
    """Stop continuous log monitoring"""
    try:
        stop_monitoring()
        return {
            "status": "success",
            "message": "Monitoring stopped"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# API route to get monitoring status
@app.get("/monitoring/status")
def monitoring_status_endpoint():
    """Get current monitoring status"""
    try:
        status = get_scheduler_status()
        return {
            "status": "success",
            "data": status
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Health check
@app.get("/health")
def health():
    return {"status": "healthy"}



