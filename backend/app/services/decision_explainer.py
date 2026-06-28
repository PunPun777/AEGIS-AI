from __future__ import annotations

from dataclasses import dataclass

from app.core.config import (
    HDE_CONFLICT_DOMAIN_FLOOR,
    HDE_PROTEST_DOMAIN_FLOOR,
    HDE_DIPLOMACY_DAMPENING_SCORE,
    HDE_CATEGORY_WEIGHTS,
)
from app.core.keyword_matcher import match_phrases, score_categories


# ── Human-readable category labels ────────────────────────────────────────────
# Used in decision_reason sentences shown to analysts.

_CATEGORY_LABELS: dict[str, str] = {
    "missile":    "missile and projectile",
    "airstrike":  "aerial strike",
    "military":   "military deployment",
    "conflict":   "active conflict",
    "terrorism":  "terrorism",
    "nuclear":    "nuclear and WMD",
    "cyber":      "cyber warfare",
    "insurgency": "insurgency",
    "coup":       "coup and overthrow",
    "weapon":     "weapons and armament",
    "shelling":   "artillery and shelling",
    "naval":      "naval confrontation",
    "casualty":   "casualty",
    "border":     "border and territorial",
    "protest":    "civil unrest and protest",
    "diplomacy":  "diplomatic",
    "economy":    "economic",
    "disaster":   "humanitarian and disaster",
}

_STRENGTH_LABELS: dict[str, str] = {
    "high":   "High-confidence",
    "medium": "Moderate",
    "low":    "Weak",
}


# ── Output dataclass ──────────────────────────────────────────────────────────

@dataclass
class DecisionExplanation:
    decision_reason: str
    matched_categories: list[str]
    matched_keywords: list[str]
    keyword_score: float
    override_score: float
    peace_dampened: bool = False


# ── Internal helpers ──────────────────────────────────────────────────────────

def _strength_label(score: float) -> str:
    if score >= 0.65:
        return "high"
    if score >= 0.30:
        return "medium"
    return "low"


def _category_phrase(categories: list[str]) -> str:
    labels = [_CATEGORY_LABELS.get(c, c) for c in categories]
    if not labels:
        return "geopolitical"
    if len(labels) == 1:
        return labels[0]
    return ", ".join(labels[:-1]) + " and " + labels[-1]


def _format_keywords(keywords: list[str], limit: int = 5) -> list[str]:
    return sorted(keywords, key=len, reverse=True)[:limit]


# ── Per-path reason builders ──────────────────────────────────────────────────

def _conflict_override_reason(
    categories: list[str],
    keywords: list[str],
    conflict_score: float,
    ml_score: float,
    indicator_count: int,
    ml_prediction: str,
    ml_confidence: float,
) -> str:
    strength = _STRENGTH_LABELS[_strength_label(conflict_score)]
    cat_phrase = _category_phrase(categories)
    kw_sample = ", ".join(f'"{k}"' for k in _format_keywords(keywords, 3))
    pct = round(ml_confidence * 100, 1)
    return (
        f"{strength} {cat_phrase} terminology detected "
        f"({indicator_count} active indicator group(s), domain score {conflict_score:.3f}). "
        f"Domain evidence outweighed ML prediction of '{ml_prediction}' "
        f"(ML score {ml_score:.3f}, confidence {pct}%). "
        f"Matched signals: {kw_sample}."
    )


def _peace_dampened_reason(
    conflict_score: float,
    peace_score: float,
    ml_score: float,
    ml_prediction: str,
) -> str:
    return (
        f"Conflict domain signals detected (score {conflict_score:.3f}, "
        f"ML score {ml_score:.3f}) but suppressed by "
        f"strong diplomatic or peace indicators (peace score {peace_score:.3f}). "
        f"ML prediction '{ml_prediction}' retained to avoid false escalation."
    )


def _protest_override_reason(
    keywords: list[str],
    protest_score: float,
    ml_score: float,
    indicator_count: int,
    ml_prediction: str,
    ml_confidence: float,
) -> str:
    strength = _STRENGTH_LABELS[_strength_label(protest_score)]
    kw_sample = ", ".join(f'"{k}"' for k in _format_keywords(keywords, 3))
    pct = round(ml_confidence * 100, 1)
    return (
        f"{strength} civil unrest and protest terminology detected "
        f"({indicator_count} indicator(s), domain score {protest_score:.3f}). "
        f"Domain evidence outweighed ML prediction of '{ml_prediction}' "
        f"(ML score {ml_score:.3f}, confidence {pct}%). "
        f"Matched signals: {kw_sample}."
    )


def _ml_retained_reason(
    ml_prediction: str,
    ml_confidence: float,
    ml_score: float,
    conflict_score: float,
    peace_score: float,
) -> str:
    pct = round(ml_confidence * 100, 1)
    if conflict_score > 0 and conflict_score <= ml_score:
        return (
            f"ML prediction '{ml_prediction}' retained (confidence {pct}%, "
            f"ML score {ml_score:.3f}). "
            f"Conflict domain signals present (score {conflict_score:.3f}) "
            f"but insufficient to outweigh ML evidence."
        )
    if peace_score >= HDE_DIPLOMACY_DAMPENING_SCORE:
        return (
            f"ML prediction '{ml_prediction}' retained (confidence {pct}%, "
            f"ML score {ml_score:.3f}). "
            f"Strong diplomatic or peace signals detected (score {peace_score:.3f}) "
            f"with no conflicting domain indicators above threshold."
        )
    return (
        f"No domain signals sufficient to challenge ML prediction "
        f"'{ml_prediction}' (confidence {pct}%, ML score {ml_score:.3f})."
    )


# ── Public builder ────────────────────────────────────────────────────────────

def build(
    text: str,
    ml_prediction: str,
    ml_confidence: float,
    outcome: str,
    ml_score: float = 0.0,
    conflict_score: float = 0.0,
    conflict_categories: list[str] | None = None,
    protest_score: float = 0.0,
    protest_keywords: list[str] | None = None,
    protest_indicators: int = 0,
    peace_score: float = 0.0,
    peace_dampened: bool = False,
    conflict_indicators: int = 0,
    conflict_category_map: dict[str, frozenset[str]] | None = None,
) -> DecisionExplanation:
    conflict_categories = conflict_categories or []
    protest_keywords = protest_keywords or []

    if outcome == "conflict_override":
        vocab = frozenset().union(*(v for v in (conflict_category_map or {}).values()))
        keywords = match_phrases(text, vocab)
        return DecisionExplanation(
            decision_reason=_conflict_override_reason(
                conflict_categories, keywords, conflict_score, ml_score,
                conflict_indicators, ml_prediction, ml_confidence,
            ),
            matched_categories=conflict_categories,
            matched_keywords=_format_keywords(keywords),
            keyword_score=conflict_score,
            override_score=conflict_score,
        )

    if outcome == "peace_dampened":
        vocab = frozenset().union(*(v for v in (conflict_category_map or {}).values()))
        keywords = match_phrases(text, vocab)
        return DecisionExplanation(
            decision_reason=_peace_dampened_reason(
                conflict_score, peace_score, ml_score, ml_prediction,
            ),
            matched_categories=conflict_categories,
            matched_keywords=_format_keywords(keywords),
            keyword_score=conflict_score,
            override_score=0.0,
            peace_dampened=True,
        )

    if outcome == "protest_override":
        return DecisionExplanation(
            decision_reason=_protest_override_reason(
                protest_keywords, protest_score, ml_score,
                protest_indicators, ml_prediction, ml_confidence,
            ),
            matched_categories=["protest"],
            matched_keywords=_format_keywords(protest_keywords),
            keyword_score=protest_score,
            override_score=protest_score,
        )

    return DecisionExplanation(
        decision_reason=_ml_retained_reason(
            ml_prediction, ml_confidence, ml_score, conflict_score, peace_score,
        ),
        matched_categories=conflict_categories,
        matched_keywords=[],
        keyword_score=conflict_score,
        override_score=0.0,
        peace_dampened=peace_dampened,
    )
