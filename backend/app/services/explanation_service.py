"""
explanation_service.py
----------------------
Generates human-readable intelligence explanations for model predictions.

All vocabulary and explanation groups are imported from the centralised
app.core.domain_knowledge module.

Matching is performed by app.core.keyword_matcher, which applies:
- Longest-phrase priority   ("missile barrage" before "missile")
- Multi-word phrase support ("exchange of fire", "armed confrontation")
- Covered-span deduplication (shorter sub-phrases in the same span are
  not reported as additional independent matches)

When a DecisionExplanation is provided (from the Hybrid Decision Engine),
its structured decision_reason is prepended to the analyst sentence list
so that the reasoning is always visible at the top of the explanation.

If no groups match, a generic fallback sentence is returned.
"""

from __future__ import annotations

from app.core.domain_knowledge import (
    CONFLICT_EXPLANATION_GROUPS,
    PROTEST_EXPLANATION_GROUPS,
    NORMAL_EXPLANATION_GROUPS,
)
from app.core.keyword_matcher import match_explanation_groups
from app.services.decision_explainer import DecisionExplanation

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


def generate_explanation(
    text: str,
    prediction: str,
    decision_explanation: DecisionExplanation | None = None,
) -> list[str]:
    groups = _EXPLANATION_GROUPS.get(prediction, [])
    sentences = match_explanation_groups(text, groups)
    if not sentences:
        sentences = [_FALLBACK_EXPLANATIONS.get(prediction, "Classification based on model output")]

    if decision_explanation and decision_explanation.decision_reason:
        reason = decision_explanation.decision_reason
        if reason not in sentences:
            sentences = [reason] + sentences

    return sentences
