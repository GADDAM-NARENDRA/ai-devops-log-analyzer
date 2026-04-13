def load_logs(file_path):
    with open(file_path, "r") as f:
        logs = f.readlines()
    return [log.strip() for log in logs]