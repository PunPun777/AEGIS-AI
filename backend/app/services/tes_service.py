PREDICTION_WEIGHTS: dict[str, float] = {
    "conflict": 1.0,
    "protest": 0.6,
    "normal": 0.2,
}

SEVERITY_MULTIPLIERS: dict[str, float] = {
    "LOW": 0.8,
    "MEDIUM": 1.0,
    "HIGH": 1.2,
    "CRITICAL": 1.5,
}

RISK_THRESHOLDS: list[tuple[float, str]] = [
    (0.91, "CRITICAL"),
    (0.61, "HIGH"),
    (0.31, "MODERATE"),
    (0.0,  "LOW"),
]


def _compute_score(events: list[dict]) -> float:
    if not events:
        return 0.0
    total = 0.0
    for e in events:
        weight = PREDICTION_WEIGHTS.get(e["prediction"], 0.0)
        confidence = e.get("confidence", 1.0)
        multiplier = SEVERITY_MULTIPLIERS.get(e.get("severity", "LOW"), 1.0)
        total += weight * confidence * multiplier
    return round(total / len(events), 4)


def _score_to_risk_level(score: float) -> str:
    for threshold, level in RISK_THRESHOLDS:
        if score >= threshold:
            return level
    return "LOW"


def calculate_tes(events: list[dict]) -> float:
    return _compute_score(events)


def get_tes_result(events: list[dict]) -> dict:
    score = _compute_score(events)
    return {
        "tes": score,
        "risk_score": score,
        "risk_level": _score_to_risk_level(score),
    }
