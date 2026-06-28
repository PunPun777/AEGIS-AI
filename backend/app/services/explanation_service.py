"""
explanation_service.py
----------------------
Generates human-readable intelligence explanations for model predictions.

All vocabulary and explanation groups are imported from the centralised
app.core.domain_knowledge module; no keyword lists are defined here.

Logic
-----
For each prediction class (conflict / protest / normal), the service
iterates over the corresponding EXPLANATION_GROUPS.  Each group is a
tuple of (frozenset[str], analyst_sentence).  If any term in the
frozenset appears in the lowercase text, the analyst sentence is
appended to the output list.

If no groups match, a generic fallback sentence is returned.
"""

from app.core.domain_knowledge import (
    CONFLICT_EXPLANATION_GROUPS,
    PROTEST_EXPLANATION_GROUPS,
    NORMAL_EXPLANATION_GROUPS,
)

_EXPLANATION_GROUPS: dict[str, list[tuple[frozenset[str], str]]] = {
    "conflict": CONFLICT_EXPLANATION_GROUPS,
    "protest":  PROTEST_EXPLANATION_GROUPS,
    "normal":   NORMAL_EXPLANATION_GROUPS,
}

_FALLBACK_EXPLANATIONS: dict[str, str] = {
    "conflict": "Geopolitical conflict indicators present",
    "protest":  "Civil unrest indicators present",
    "normal":   "No significant threat indicators detected",
}


def generate_explanation(text: str, prediction: str) -> list[str]:
    lower = text.lower()
    groups = _EXPLANATION_GROUPS.get(prediction, [])
    explanations = [
        sentence
        for keywords, sentence in groups
        if any(kw in lower for kw in keywords)
    ]
    if not explanations:
        explanations = [_FALLBACK_EXPLANATIONS.get(prediction, "Classification based on model output")]
    return explanations
