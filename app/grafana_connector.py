import requests
from datetime import datetime
from typing import List, Dict

class GrafanaConnector:
    def __init__(self, grafana_url: str = "http://localhost:3000", api_key: str = None):
        self.grafana_url = grafana_url.rstrip("/")
        self.api_key = api_key or ""
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } if api_key else {"Content-Type": "application/json"}
    
    def get_datasources(self) -> List[Dict]:
        """Get list of data sources from Grafana"""
        try:
            endpoint = f"{self.grafana_url}/api/datasources"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            
            if response.status_code == 401:
                return [{"error": "Authentication failed - API key required"}]
            
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return [{"error": f"Failed to fetch datasources: {str(e)}"}]
    
    def get_dashboards(self) -> List[Dict]:
        """Get list of dashboards from Grafana"""
        try:
            endpoint = f"{self.grafana_url}/api/search"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return [{"error": f"Failed to fetch dashboards: {str(e)}"}]
    
    def get_dashboard(self, dashboard_id: int) -> Dict:
        """Get specific dashboard details"""
        try:
            endpoint = f"{self.grafana_url}/api/dashboards/db/{dashboard_id}"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": f"Failed to fetch dashboard: {str(e)}"}
    
    def get_annotations(self, hours: int = 24) -> List[Dict]:
        """Get annotations/events from Grafana"""
        try:
            endpoint = f"{self.grafana_url}/api/annotations"
            
            # Grafana uses millisecond timestamps
            from_time = int((datetime.now().timestamp() - hours * 3600) * 1000)
            to_time = int(datetime.now().timestamp() * 1000)
            
            params = {
                "from": from_time,
                "to": to_time,
                "limit": 100
            }
            
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return [{"error": f"Failed to fetch annotations: {str(e)}"}]
    
    def fetch_all_data(self, hours: int = 24) -> str:
        """Fetch Grafana data sources, dashboards, and annotations"""
        formatted_logs = [f"Grafana Data - {datetime.now().isoformat()}"]
        
        # Datasources
        formatted_logs.append("\n=== Datasources ===")
        datasources = self.get_datasources()
        if datasources and "error" not in str(datasources):
            for ds in datasources[:10]:
                ds_type = ds.get("type", "unknown")
                ds_name = ds.get("name", "unknown")
                formatted_logs.append(f"[DATASOURCE] {ds_name} ({ds_type})")
        else:
            formatted_logs.append("Note: No API key provided - some data unavailable")
        
        # Dashboards
        formatted_logs.append("\n=== Dashboards ===")
        dashboards = self.get_dashboards()
        if dashboards and "error" not in str(dashboards):
            for db in dashboards[:10]:
                db_title = db.get("title", "unknown")
                db_type = db.get("type", "unknown")
                formatted_logs.append(f"[DASHBOARD] {db_title} ({db_type})")
        
        # Annotations
        formatted_logs.append("\n=== Annotations/Events ===")
        annotations = self.get_annotations(hours=hours)
        if annotations and "error" not in str(annotations):
            for annotation in annotations[:20]:
                text = annotation.get("text", "")
                timestamp = annotation.get("time", 0)
                dt = datetime.fromtimestamp(timestamp / 1000)
                formatted_logs.append(f"[ANNOTATION] {dt.isoformat()}: {text}")
        
        return "\n".join(formatted_logs)
