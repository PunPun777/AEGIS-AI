from __future__ import annotations

from dataclasses import dataclass, field

from app.core.config import (
    HDE_CONFLICT_DOMAIN_FLOOR,
    HDE_DIPLOMACY_DAMPENING_SCORE,
    HDE_CATEGORY_WEIGHTS,
    HDE_CONTEXT_WEIGHTS,
    HDE_DOMINANT_CONTRAST_THRESHOLD,
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

# Context groups: each maps a broad geopolitical context name to its member categories.
# Used to aggregate weighted scores and determine the dominant context.
_CONTEXT_GROUPS: dict[str, list[str]] = {
    "conflict": [
        "missile", "airstrike", "military", "conflict", "terrorism",
        "nuclear", "cyber", "insurgency", "coup", "weapon", "shelling",
        "naval", "casualty", "border",
    ],
    "protest": ["protest"],
    "peace":   ["diplomacy", "economy", "disaster"],
}

# Dominant-context prose templates keyed by (dominant_context, secondary_context).
_DOMINANT_PROSE: dict[tuple[str, str], str] = {
    ("conflict", "peace"):   (
        "Conflict indicators significantly outweighed diplomatic or peace terminology."
    ),
    ("conflict", "protest"): (
        "Conflict and military indicators dominated over civil unrest signals."
    ),
    ("protest", "conflict"): (
        "Civil unrest indicators dominated despite the presence of security-related language."
    ),
    ("protest", "peace"):    (
        "Protest activity dominated over diplomatic or economic context."
    ),
    ("peace", "conflict"):   (
        "Diplomatic and peace signals were present alongside conflict terminology; "
        "de-escalation context is dominant."
    ),
    ("peace", "protest"):    (
        "Diplomatic or economic context dominated over civil-unrest signals."
    ),
}

# Dominant-category lead sentences keyed by the dominant category name.
_LEAD_SENTENCES: dict[str, str] = {
    "missile":    "Missile or projectile indicators are the primary geopolitical signal.",
    "airstrike":  "Aerial strike activity is the primary geopolitical signal.",
    "terrorism":  "Terrorism indicators represent the primary threat signal.",
    "nuclear":    "Nuclear or WMD language constitutes the primary geopolitical signal.",
    "military":   "Military escalation involving nation-state actors detected.",
    "shelling":   "Heavy artillery or shelling activity is the primary signal.",
    "conflict":   "Active armed conflict language is the primary geopolitical signal.",
    "insurgency": "Insurgency or guerrilla activity is the primary geopolitical signal.",
    "coup":       "Coup or governmental overthrow language is the primary signal.",
    "weapon":     "Weapons and armament context is the primary geopolitical signal.",
    "naval":      "Naval confrontation is the primary geopolitical signal.",
    "cyber":      "Cyber warfare indicators are the primary geopolitical signal.",
    "casualty":   "Casualty and human-loss language is the primary geopolitical signal.",
    "border":     "Border tensions or territorial dispute is the primary geopolitical signal.",
    "protest":    "Civil unrest and protest activity is the primary geopolitical signal.",
    "diplomacy":  "Diplomatic engagement is the dominant geopolitical context.",
    "economy":    "Economic and trade context is the dominant geopolitical frame.",
    "disaster":   "Humanitarian or disaster response is the dominant geopolitical context.",
}


# ── Output dataclass ──────────────────────────────────────────────────────────

@dataclass
class DecisionExplanation:
    decision_reason: str
    dominant_category: str
    matched_categories: list[str]
    matched_keywords: list[str]
    keyword_score: float
    override_score: float
    category_scores: dict[str, float] = field(default_factory=dict)
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


def _dominant_context_analysis(
    active_categories: list[str],
    category_scores: dict[str, float],
) -> tuple[str, str, str, str]:
    """
    Given the active categories and their raw scores, compute:
    - dominant_category : the single highest-weighted active category
    - dominant_context  : "conflict" | "protest" | "peace" | "none"
    - secondary_context : the second-highest context (may be "")
    - contrast_sentence : prose describing how dominant beats secondary (may be "")
    """
    if not active_categories:
        return "", "none", "", ""

    # Weighted score per category
    cat_weighted: dict[str, float] = {
        c: category_scores.get(c, 0.0) * HDE_CONTEXT_WEIGHTS.get(c, 1)
        for c in active_categories
    }

    dominant_category = max(cat_weighted, key=lambda c: cat_weighted[c])

    # Aggregate into context groups
    context_scores: dict[str, float] = {}
    for ctx, members in _CONTEXT_GROUPS.items():
        context_scores[ctx] = sum(
            cat_weighted.get(m, 0.0) for m in members if m in active_categories
        )

    ranked = sorted(context_scores.items(), key=lambda x: x[1], reverse=True)
    dominant_context = ranked[0][0] if ranked else "none"
    dominant_ctx_score = ranked[0][1] if ranked else 0.0

    secondary_context = ""
    contrast_sentence = ""
    if len(ranked) >= 2 and ranked[1][1] > 0:
        second_ctx = ranked[1][0]
        second_score = ranked[1][1]
        if dominant_ctx_score - second_score >= HDE_DOMINANT_CONTRAST_THRESHOLD:
            secondary_context = second_ctx
            contrast_sentence = _DOMINANT_PROSE.get(
                (dominant_context, secondary_context), ""
            )

    return dominant_category, dominant_context, secondary_context, contrast_sentence


# ── Per-path reason builders ──────────────────────────────────────────────────

def _conflict_override_reason(
    categories: list[str],
    keywords: list[str],
    conflict_score: float,
    ml_score: float,
    indicator_count: int,
    ml_prediction: str,
    ml_confidence: float,
    dominant_category: str,
    contrast_sentence: str,
) -> str:
    strength = _STRENGTH_LABELS[_strength_label(conflict_score)]
    lead = _LEAD_SENTENCES.get(dominant_category, f"{_CATEGORY_LABELS.get(dominant_category, dominant_category)} indicators detected.")
    kw_sample = ", ".join(f'"{k}"' for k in _format_keywords(keywords, 3))
    pct = round(ml_confidence * 100, 1)
    parts = [
        f"{lead} {strength} domain evidence ({indicator_count} active group(s), "
        f"score {conflict_score:.3f}) outweighed ML prediction of '{ml_prediction}' "
        f"(ML score {ml_score:.3f}, confidence {pct}%). "
        f"Key signals: {kw_sample}."
    ]
    if contrast_sentence:
        parts.append(contrast_sentence)
    return " ".join(parts)


def _peace_dampened_reason(
    conflict_score: float,
    peace_score: float,
    ml_score: float,
    ml_prediction: str,
    dominant_category: str,
) -> str:
    lead = _LEAD_SENTENCES.get(dominant_category, "Conflict signals detected.")
    return (
        f"{lead} However, strong diplomatic or peace signals (score {peace_score:.3f}) "
        f"suppressed the conflict domain evidence (score {conflict_score:.3f}, "
        f"ML score {ml_score:.3f}). "
        f"ML prediction '{ml_prediction}' retained to avoid false escalation."
    )


def _protest_override_reason(
    keywords: list[str],
    protest_score: float,
    ml_score: float,
    indicator_count: int,
    ml_prediction: str,
    ml_confidence: float,
    contrast_sentence: str,
) -> str:
    strength = _STRENGTH_LABELS[_strength_label(protest_score)]
    kw_sample = ", ".join(f'"{k}"' for k in _format_keywords(keywords, 3))
    pct = round(ml_confidence * 100, 1)
    parts = [
        f"Civil unrest and protest activity is the primary geopolitical signal. "
        f"{strength} protest evidence ({indicator_count} indicator(s), "
        f"score {protest_score:.3f}) outweighed ML prediction of '{ml_prediction}' "
        f"(ML score {ml_score:.3f}, confidence {pct}%). "
        f"Key signals: {kw_sample}."
    ]
    if contrast_sentence:
        parts.append(contrast_sentence)
    return " ".join(parts)


def _ml_retained_reason(
    ml_prediction: str,
    ml_confidence: float,
    ml_score: float,
    conflict_score: float,
    peace_score: float,
    dominant_category: str,
    contrast_sentence: str,
) -> str:
    pct = round(ml_confidence * 100, 1)
    if conflict_score > 0 and conflict_score <= ml_score:
        lead = _LEAD_SENTENCES.get(dominant_category, "Domain signals detected.")
        parts = [
            f"{lead} ML prediction '{ml_prediction}' retained "
            f"(confidence {pct}%, ML score {ml_score:.3f}). "
            f"Conflict domain signals present (score {conflict_score:.3f}) "
            f"but insufficient to outweigh ML evidence."
        ]
        if contrast_sentence:
            parts.append(contrast_sentence)
        return " ".join(parts)
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
    category_scores: dict[str, float] | None = None,
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
    category_scores = category_scores or {}

    dominant_category, dominant_context, secondary_context, contrast = (
        _dominant_context_analysis(conflict_categories, category_scores)
        if conflict_categories
        else ("", "none", "", "")
    )

    if outcome == "conflict_override":
        vocab = frozenset().union(*(v for v in (conflict_category_map or {}).values()))
        keywords = match_phrases(text, vocab)
        return DecisionExplanation(
            decision_reason=_conflict_override_reason(
                conflict_categories, keywords, conflict_score, ml_score,
                conflict_indicators, ml_prediction, ml_confidence,
                dominant_category, contrast,
            ),
            dominant_category=dominant_category,
            matched_categories=conflict_categories,
            matched_keywords=_format_keywords(keywords),
            keyword_score=conflict_score,
            override_score=conflict_score,
            category_scores=category_scores,
        )

    if outcome == "peace_dampened":
        vocab = frozenset().union(*(v for v in (conflict_category_map or {}).values()))
        keywords = match_phrases(text, vocab)
        return DecisionExplanation(
            decision_reason=_peace_dampened_reason(
                conflict_score, peace_score, ml_score, ml_prediction, dominant_category,
            ),
            dominant_category=dominant_category,
            matched_categories=conflict_categories,
            matched_keywords=_format_keywords(keywords),
            keyword_score=conflict_score,
            override_score=0.0,
            category_scores=category_scores,
            peace_dampened=True,
        )

    if outcome == "protest_override":
        p_cats = ["protest"]
        _, _, p_secondary, p_contrast = _dominant_context_analysis(
            p_cats, {"protest": protest_score}
        )
        return DecisionExplanation(
            decision_reason=_protest_override_reason(
                protest_keywords, protest_score, ml_score,
                protest_indicators, ml_prediction, ml_confidence, p_contrast,
            ),
            dominant_category="protest",
            matched_categories=p_cats,
            matched_keywords=_format_keywords(protest_keywords),
            keyword_score=protest_score,
            override_score=protest_score,
            category_scores={"protest": protest_score},
        )

    return DecisionExplanation(
        decision_reason=_ml_retained_reason(
            ml_prediction, ml_confidence, ml_score,
            conflict_score, peace_score, dominant_category, contrast,
        ),
        dominant_category=dominant_category,
        matched_categories=conflict_categories,
        matched_keywords=[],
        keyword_score=conflict_score,
        override_score=0.0,
        category_scores=category_scores,
        peace_dampened=peace_dampened,
    )
