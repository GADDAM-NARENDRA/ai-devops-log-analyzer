import requests
from datetime import datetime, timedelta
from typing import List, Dict

class LokiConnector:
    def __init__(self, loki_url: str = "http://localhost:3100"):
        self.loki_url = loki_url.rstrip("/")
    
    def query_logs(self, query_string: str = '{job=~".+"}', hours: int = 24, limit: int = 1000) -> List[str]:
        """
        Query logs from Loki using LogQL
        
        Args:
            query_string: LogQL query (default returns all logs)
            hours: How many hours back to query
            limit: Maximum number of log lines to return
        
        Returns:
            List of formatted log strings
        """
        try:
            endpoint = f"{self.loki_url}/loki/api/v1/query_range"
            
            start_time = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1e9)
            end_time = int(datetime.now().timestamp() * 1e9)
            
            params = {
                "query": query_string,
                "start": start_time,
                "end": end_time,
                "limit": limit
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logs = []
            
            # Parse Loki response format
            if data.get("status") == "success":
                result = data.get("data", {}).get("result", [])
                for stream in result:
                    labels = stream.get("values", [])
                    for timestamp, log_line in labels:
                        # Convert nanosecond timestamp to readable format
                        dt = datetime.fromtimestamp(int(timestamp) / 1e9)
                        formatted_log = f"{dt.isoformat()} [LOKI] {log_line}"
                        logs.append(formatted_log)
            
            return logs
        
        except Exception as e:
            return [f"ERROR: Failed to fetch Loki logs - {str(e)}"]
    
    def fetch_all_logs(self, hours: int = 24) -> str:
        """Fetch all logs and return as formatted string"""
        logs = self.query_logs(hours=hours)
        return "\n".join(logs) if logs else "No logs found in Loki"
