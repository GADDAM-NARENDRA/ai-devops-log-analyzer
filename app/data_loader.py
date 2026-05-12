import os
from pathlib import Path

def load_logs(file_path=None):
    """
    Load logs from a single file or all .log files from data folder
    
    Args:
        file_path: Specific file to load (e.g., "data/sample_logs.txt")
                   If None, loads all .log files from data folder
    
    Returns:
        List of log strings
    """
    if file_path:
        # Load from specific file
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                logs = f.readlines()
            return [log.strip() for log in logs if log.strip()]
        else:
            return [f"Error: File not found - {file_path}"]
    
    # Load from all files in data folder
    data_dir = "data"
    all_logs = []
    
    if not os.path.exists(data_dir):
        return ["Error: data folder not found"]
    
    # Load all .log and .txt files
    for file_path in Path(data_dir).glob("*"):
        if file_path.is_file() and (file_path.suffix in ['.log', '.txt']):
            try:
                with open(file_path, "r") as f:
                    logs = f.readlines()
                
                # Add source identifier
                source = file_path.name
                for log in logs:
                    log = log.strip()
                    if log:
                        all_logs.append(f"[{source}] {log}")
            
            except Exception as e:
                all_logs.append(f"Error reading {file_path.name}: {str(e)}")
    
    return all_logs if all_logs else ["No log files found in data folder"]
