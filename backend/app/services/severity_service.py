"""
severity_service.py
-------------------
Derives a rule-based severity level for a classified event.

All vocabulary is imported from the centralised
app.core.domain_knowledge module; no keyword lists are defined here.

Severity rules
--------------
- conflict   → CRITICAL   if any CRITICAL_SEVERITY_TRIGGER term is found
- conflict   → HIGH       otherwise
- protest    → MEDIUM
- normal     → LOW
"""

from app.core.domain_knowledge import CRITICAL_SEVERITY_TRIGGERS

SEVERITY_MAP: dict[str, str] = {
    "normal": "LOW",
    "protest": "MEDIUM",
    "conflict": "HIGH",
}


def get_severity(prediction: str, text: str) -> str:
    if prediction == "conflict":
        lower = text.lower()
        if any(trigger in lower for trigger in CRITICAL_SEVERITY_TRIGGERS):
            return "CRITICAL"
        return "HIGH"
    return SEVERITY_MAP.get(prediction, "LOW")
