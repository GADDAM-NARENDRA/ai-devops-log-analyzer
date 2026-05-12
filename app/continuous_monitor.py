"""
Continuous log monitoring with APScheduler
Fetches logs from Loki, Prometheus, Grafana every 15 minutes
"""

import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.fetch_logs import fetch_and_save_all_logs
from app.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None

def start_monitoring(interval_minutes: int = 15, grafana_api_key: str = None):
    """
    Start continuous log monitoring
    
    Args:
        interval_minutes: Fetch logs every N minutes (default: 15)
        grafana_api_key: Optional Grafana API key
    """
    global scheduler
    
    if scheduler and scheduler.running:
        logger.warning("Scheduler is already running")
        return
    
    scheduler = BackgroundScheduler()
    
    # Add job to fetch logs
    scheduler.add_job(
        func=scheduled_fetch_logs,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id='fetch_logs_job',
        name=f'Fetch logs every {interval_minutes} minutes',
        replace_existing=True,
        args=[grafana_api_key]
    )
    
    scheduler.start()
    logger.info(f"✅ Monitoring started - fetching logs every {interval_minutes} minutes")
    print(f"[{datetime.now().isoformat()}] ✅ Monitoring started - fetching logs every {interval_minutes} minutes")

def stop_monitoring():
    """Stop continuous log monitoring"""
    global scheduler
    
    if scheduler and scheduler.running:
        scheduler.shutdown()
        logger.info("✅ Monitoring stopped")
        print(f"[{datetime.now().isoformat()}] ✅ Monitoring stopped")
    else:
        logger.warning("Scheduler is not running")

def get_scheduler_status():
    """Get current scheduler status"""
    if not scheduler:
        return {
            "running": False,
            "jobs": []
        }
    
    return {
        "running": scheduler.running,
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run_time": str(job.next_run_time)
            }
            for job in scheduler.get_jobs()
        ]
    }

def scheduled_fetch_logs(grafana_api_key: str = None):
    """Scheduled task to fetch logs"""
    try:
        print(f"\n[{datetime.now().isoformat()}] 📥 Fetching logs from Loki, Prometheus, Grafana...")
        logger.info("Fetching logs from all sources...")
        
        fetch_and_save_all_logs(
            hours=1,  # Fetch last 1 hour to get fresh data
            grafana_api_key=grafana_api_key or settings.GRAFANA_API_KEY
        )
        
        logger.info("✅ Successfully fetched logs from all sources")
        print(f"[{datetime.now().isoformat()}] ✅ Log fetch completed")
    
    except Exception as e:
        logger.error(f"❌ Error fetching logs: {str(e)}")
        print(f"[{datetime.now().isoformat()}] ❌ Error: {str(e)}")

if __name__ == "__main__":
    import time
    
    print("Starting continuous log monitoring...")
    print("Press Ctrl+C to stop\n")
    
    # Start monitoring every 15 minutes
    start_monitoring(interval_minutes=15)
    
    # Fetch immediately on startup
    scheduled_fetch_logs()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        stop_monitoring()
        print("✅ Monitoring stopped")
