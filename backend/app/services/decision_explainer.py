from __future__ import annotations

from dataclasses import dataclass, field

from app.core.config import (
    HDE_ML_TRUST_THRESHOLD,
    HDE_CONFLICT_OVERRIDE_SCORE,
    HDE_PROTEST_OVERRIDE_SCORE,
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
    if score >= 0.35:
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

def _ml_trusted_reason(ml_prediction: str, ml_confidence: float) -> str:
    pct = round(ml_confidence * 100, 1)
    return (
        f"Prediction retained because ML confidence ({pct}%) exceeded the "
        f"override threshold ({round(HDE_ML_TRUST_THRESHOLD * 100)}%). "
        f"Domain signals were not evaluated."
    )


def _conflict_override_reason(
    categories: list[str],
    keywords: list[str],
    conflict_score: float,
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
        f"({indicator_count} active indicator group(s), score {conflict_score:.3f}). "
        f"Multiple conflict indicators outweighed the ML prediction of "
        f"'{ml_prediction}' (confidence {pct}%). "
        f"Matched signals: {kw_sample}."
    )


def _peace_dampened_reason(
    conflict_score: float,
    peace_score: float,
    ml_prediction: str,
) -> str:
    return (
        f"Conflict signals detected (score {conflict_score:.3f}) but suppressed by "
        f"strong diplomatic or peace indicators (peace score {peace_score:.3f}). "
        f"ML prediction '{ml_prediction}' retained to avoid false escalation."
    )


def _protest_override_reason(
    keywords: list[str],
    protest_score: float,
    indicator_count: int,
    ml_confidence: float,
) -> str:
    strength = _STRENGTH_LABELS[_strength_label(protest_score)]
    kw_sample = ", ".join(f'"{k}"' for k in _format_keywords(keywords, 3))
    pct = round(ml_confidence * 100, 1)
    return (
        f"{strength} civil unrest and protest terminology detected "
        f"({indicator_count} indicator(s), score {protest_score:.3f}). "
        f"ML prediction 'normal' (confidence {pct}%) overridden to 'protest'. "
        f"Matched signals: {kw_sample}."
    )


def _prediction_kept_reason(
    ml_prediction: str,
    ml_confidence: float,
    conflict_score: float,
    peace_dampened: bool,
) -> str:
    pct = round(ml_confidence * 100, 1)
    if peace_dampened:
        return _peace_dampened_reason(conflict_score, 0.0, ml_prediction)
    if conflict_score > 0:
        return (
            f"Conflict signals present (score {conflict_score:.3f}) but below the "
            f"override threshold ({HDE_CONFLICT_OVERRIDE_SCORE:.2f}). "
            f"ML prediction '{ml_prediction}' (confidence {pct}%) retained."
        )
    return (
        f"No significant domain signals detected. "
        f"ML prediction '{ml_prediction}' (confidence {pct}%) accepted as-is."
    )


# ── Public builder ────────────────────────────────────────────────────────────

def build(
    text: str,
    ml_prediction: str,
    ml_confidence: float,
    outcome: str,
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

    if outcome == "ml_trusted":
        return DecisionExplanation(
            decision_reason=_ml_trusted_reason(ml_prediction, ml_confidence),
            matched_categories=[],
            matched_keywords=[],
            keyword_score=0.0,
            override_score=0.0,
        )

    if outcome == "conflict_override":
        vocab = frozenset().union(*(v for v in (conflict_category_map or {}).values()))
        keywords = match_phrases(text, vocab)
        return DecisionExplanation(
            decision_reason=_conflict_override_reason(
                conflict_categories, keywords, conflict_score,
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
            decision_reason=_peace_dampened_reason(conflict_score, peace_score, ml_prediction),
            matched_categories=conflict_categories,
            matched_keywords=_format_keywords(keywords),
            keyword_score=conflict_score,
            override_score=0.0,
            peace_dampened=True,
        )

    if outcome == "protest_override":
        return DecisionExplanation(
            decision_reason=_protest_override_reason(
                protest_keywords, protest_score, protest_indicators, ml_confidence,
            ),
            matched_categories=["protest"],
            matched_keywords=_format_keywords(protest_keywords),
            keyword_score=protest_score,
            override_score=protest_score,
        )

    # outcome == "kept"
    return DecisionExplanation(
        decision_reason=_prediction_kept_reason(
            ml_prediction, ml_confidence, conflict_score, peace_dampened,
        ),
        matched_categories=conflict_categories,
        matched_keywords=[],
        keyword_score=conflict_score,
        override_score=0.0,
        peace_dampened=peace_dampened,
    )
