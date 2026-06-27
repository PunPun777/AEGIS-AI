CRITICAL_KEYWORDS: frozenset[str] = frozenset({
    "missile",
    "airstrike",
    "explosion",
    "terror",
    "invasion",
    "war",
})

SEVERITY_MAP: dict[str, str] = {
    "normal": "LOW",
    "protest": "MEDIUM",
    "conflict": "HIGH",
}


def get_severity(prediction: str, text: str) -> str:
    if prediction == "conflict":
        lower = text.lower()
        if any(keyword in lower for keyword in CRITICAL_KEYWORDS):
            return "CRITICAL"
        return "HIGH"
    return SEVERITY_MAP.get(prediction, "LOW")
