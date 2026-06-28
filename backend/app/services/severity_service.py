"""
severity_service.py
-------------------
Derives a rule-based severity level for a classified event.

All vocabulary is imported from the centralised
app.core.domain_knowledge module.

Matching is performed by app.core.keyword_matcher, which applies
longest-phrase priority and covered-span deduplication.  This means
compound phrases such as "missile barrage" or "air defence system"
are recognised correctly without double-counting sub-tokens.

Severity rules
--------------
- conflict   → CRITICAL   if any CRITICAL_SEVERITY_TRIGGER phrase matches
- conflict   → HIGH       otherwise
- protest    → MEDIUM
- normal     → LOW
"""

from app.core.domain_knowledge import CRITICAL_SEVERITY_TRIGGERS
from app.core.keyword_matcher import has_match

SEVERITY_MAP: dict[str, str] = {
    "normal": "LOW",
    "protest": "MEDIUM",
    "conflict": "HIGH",
}


def get_severity(prediction: str, text: str) -> str:
    if prediction == "conflict":
        if has_match(text, CRITICAL_SEVERITY_TRIGGERS):
            return "CRITICAL"
        return "HIGH"
    return SEVERITY_MAP.get(prediction, "LOW")
