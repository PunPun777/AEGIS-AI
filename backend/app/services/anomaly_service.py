ANOMALY_THRESHOLD = 0.6

def detect_anomaly(events: list[dict]) -> bool:
    if not events:
        return False
    high_severity = sum(1 for e in events if e["prediction"] in ("conflict", "protest"))
    return (high_severity / len(events)) > ANOMALY_THRESHOLD
