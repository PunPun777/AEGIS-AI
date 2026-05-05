WEIGHTS: dict[str, float] = {
    "conflict": 1.0,
    "protest": 0.6,
    "normal": 0.2,
}

def calculate_tes(events: list[dict]) -> float:
    if not events:
        return 0.0
    total = sum(WEIGHTS.get(e["prediction"], 0.0) for e in events)
    return round(total / len(events), 2)
