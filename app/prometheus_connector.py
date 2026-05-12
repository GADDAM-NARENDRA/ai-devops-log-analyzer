import requests
from datetime import datetime, timedelta
from typing import List, Dict

class PrometheusConnector:
    def __init__(self, prometheus_url: str = "http://localhost:9090"):
        self.prometheus_url = prometheus_url.rstrip("/")
    
    def query_metrics(self, promql_query: str) -> Dict:
        """
        Query metrics from Prometheus
        
        Args:
            promql_query: PromQL query expression
        
        Returns:
            Query result dictionary
        """
        try:
            endpoint = f"{self.prometheus_url}/api/v1/query"
            params = {"query": promql_query}
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            return {"error": f"Failed to query Prometheus: {str(e)}"}
    
    def query_range_metrics(self, promql_query: str, hours: int = 24, step: str = "5m") -> Dict:
        """
        Query metrics over a time range
        
        Args:
            promql_query: PromQL query expression
            hours: How many hours back to query
            step: Resolution step (e.g., '5m', '1m')
        
        Returns:
            Query result dictionary
        """
        try:
            endpoint = f"{self.prometheus_url}/api/v1/query_range"
            
            start_time = int((datetime.now() - timedelta(hours=hours)).timestamp())
            end_time = int(datetime.now().timestamp())
            
            params = {
                "query": promql_query,
                "start": start_time,
                "end": end_time,
                "step": step
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            return {"error": f"Failed to query Prometheus range: {str(e)}"}
    
    def get_alerts(self) -> List[Dict]:
        """Get active alerts from Prometheus"""
        try:
            endpoint = f"{self.prometheus_url}/api/v1/alerts"
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("data", {}).get("alerts", [])
        
        except Exception as e:
            return [{"error": f"Failed to fetch alerts: {str(e)}"}]
    
    def fetch_all_metrics(self, hours: int = 24) -> str:
        """Fetch various metrics and return as formatted string"""
        metrics_queries = [
            ('up{job="prometheus"}', "Prometheus Up Status"),
            ('node_cpu_seconds_total', "CPU Seconds"),
            ('node_memory_MemAvailable_bytes', "Memory Available"),
            ('container_cpu_usage_seconds_total', "Container CPU Usage"),
            ('container_memory_usage_bytes', "Container Memory Usage"),
        ]
        
        formatted_logs = [f"Prometheus Metrics - {datetime.now().isoformat()}"]
        
        # Add alerts
        alerts = self.get_alerts()
        if alerts:
            formatted_logs.append("\n=== Active Alerts ===")
            for alert in alerts:
                state = alert.get("state", "unknown")
                labels = alert.get("labels", {})
                formatted_logs.append(f"[ALERT] {state}: {labels}")
        
        # Query metrics
        formatted_logs.append("\n=== Metrics ===")
        for query, label in metrics_queries:
            result = self.query_range_metrics(query, hours=hours)
            if result.get("status") == "success":
                data = result.get("data", {}).get("result", [])
                if data:
                    formatted_logs.append(f"\n{label}:")
                    for metric in data[:5]:  # Limit to 5 results per query
                        metric_name = metric.get("metric", {})
                        values = metric.get("values", [])
                        if values:
                            latest_value = values[-1]
                            formatted_logs.append(f"  {metric_name}: {latest_value[1]}")
        
        return "\n".join(formatted_logs)
