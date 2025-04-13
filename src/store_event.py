import json
from datetime import datetime

def log_high_risk_event(data, path="utils/high_risk_history.json"):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        **data
    }
    try:
        with open(path, "r") as f:
            log = json.load(f)
    except FileNotFoundError:
        log = []

    log.append(event)
    with open(path, "w") as f:
        json.dump(log, f, indent=4)
