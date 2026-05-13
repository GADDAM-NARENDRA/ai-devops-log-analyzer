"""
Script to fetch logs from Loki, Prometheus, and Grafana and save to data folder
Run: python app/fetch_logs.py
"""

import os
from datetime import datetime
from app.loki_connector import LokiConnector
from app.prometheus_connector import PrometheusConnector
from app.grafana_connector import GrafanaConnector
from app.config import settings

def fetch_and_save_all_logs(hours: int = 24, grafana_api_key: str = None):
    """
    Fetch logs from all sources and save to data folder
    
    Args:
        hours: How many hours back to fetch
        grafana_api_key: Optional Grafana API key
    """
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"[{datetime.now().isoformat()}] Starting log fetch...")
    
    # 1. Fetch Loki logs
    print("[1/3] Fetching Loki logs...")
    try:
        loki = LokiConnector(
            loki_url=getattr(settings, 'LOKI_URL', 'http://localhost:3100')
        )
        loki_logs = loki.fetch_all_logs(hours=hours)
        loki_path = os.path.join(data_dir, "loki.log")
        with open(loki_path, "a") as f:
            f.write(loki_logs)
        print(f"✅ Loki logs appended to {loki_path}")
    except Exception as e:
        print(f"❌ Error fetching Loki logs: {e}")
    
    # 2. Fetch Prometheus metrics
    print("[2/3] Fetching Prometheus metrics...")
    try:
        prometheus = PrometheusConnector(
            prometheus_url=getattr(settings, 'PROMETHEUS_URL', 'http://localhost:9090')
        )
        prometheus_metrics = prometheus.fetch_all_metrics(hours=hours)
        prometheus_path = os.path.join(data_dir, "prometheus.log")
        with open(prometheus_path, "a") as f:
            f.write(prometheus_metrics)
        print(f"✅ Prometheus metrics appended to {prometheus_path}")
    except Exception as e:
        print(f"❌ Error fetching Prometheus metrics: {e}")
    
    # 3. Fetch Grafana data
    print("[3/3] Fetching Grafana data...")
    try:
        grafana = GrafanaConnector(
            grafana_url=getattr(settings, 'GRAFANA_URL', 'http://localhost:3000'),
            api_key=grafana_api_key or getattr(settings, 'GRAFANA_API_KEY', None)
        )
        grafana_data = grafana.fetch_all_data(hours=hours)
        grafana_path = os.path.join(data_dir, "grafana.log")
        with open(grafana_path, "a") as f:
            f.write(grafana_data)
        print(f"✅ Grafana data appended to {grafana_path}")
    except Exception as e:
        print(f"❌ Error fetching Grafana data: {e}")
    
    print(f"[{datetime.now().isoformat()}] ✅ Log fetch completed!")
    print(f"\nLogs saved in: {os.path.abspath(data_dir)}/")
    print("  - loki.log")
    print("  - prometheus.log")
    print("  - grafana.log")
    print("  - sample_logs.txt (original)")

if __name__ == "__main__":
    import sys
    
    hours = 24
    grafana_api_key = None
    
    if len(sys.argv) > 1:
        hours = int(sys.argv[1])
    if len(sys.argv) > 2:
        grafana_api_key = sys.argv[2]
    
    fetch_and_save_all_logs(hours=hours, grafana_api_key=grafana_api_key)
