from __future__ import annotations

from dataclasses import dataclass

from app.core.config import (
    HDE_ML_TRUST_THRESHOLD,
    HDE_LOW_CONFIDENCE_THRESHOLD,
    HDE_SCORE_CAP,
    HDE_CONFLICT_OVERRIDE_SCORE,
    HDE_PROTEST_OVERRIDE_SCORE,
    HDE_DIPLOMACY_DAMPENING_SCORE,
    HDE_MIN_INDICATORS_MEDIUM,
    HDE_MIN_INDICATORS_LOW,
    HDE_CATEGORY_WEIGHTS,
)
from app.core.domain_knowledge import (
    ALL_CONFLICT_KEYWORDS,
    ALL_PROTEST_KEYWORDS,
    DIPLOMACY_KEYWORDS,
    PEACE_KEYWORDS,
    ECONOMY_KEYWORDS,
    DISASTER_KEYWORDS,
    MISSILE_KEYWORDS,
    AIRSTRIKE_KEYWORDS,
    MILITARY_KEYWORDS,
    CONFLICT_KEYWORDS,
    TERRORISM_KEYWORDS,
    NUCLEAR_KEYWORDS,
    CYBER_KEYWORDS,
    INSURGENCY_KEYWORDS,
    COUP_KEYWORDS,
    WEAPON_KEYWORDS,
    SHELLING_KEYWORDS,
    NAVAL_KEYWORDS,
    CASUALTY_KEYWORDS,
    BORDER_KEYWORDS,
    PROTEST_KEYWORDS,
)
from app.core.keyword_matcher import match_phrases, score_categories


# ── Category maps ─────────────────────────────────────────────────────────────

_CONFLICT_CATEGORY_MAP: dict[str, frozenset[str]] = {
    "missile":    MISSILE_KEYWORDS,
    "airstrike":  AIRSTRIKE_KEYWORDS,
    "military":   MILITARY_KEYWORDS,
    "conflict":   CONFLICT_KEYWORDS,
    "terrorism":  TERRORISM_KEYWORDS,
    "nuclear":    NUCLEAR_KEYWORDS,
    "cyber":      CYBER_KEYWORDS,
    "insurgency": INSURGENCY_KEYWORDS,
    "coup":       COUP_KEYWORDS,
    "weapon":     WEAPON_KEYWORDS,
    "shelling":   SHELLING_KEYWORDS,
    "naval":      NAVAL_KEYWORDS,
    "casualty":   CASUALTY_KEYWORDS,
    "border":     BORDER_KEYWORDS,
}

_PROTEST_CATEGORY_MAP: dict[str, frozenset[str]] = {
    "protest": PROTEST_KEYWORDS,
}

_PEACE_CATEGORY_MAP: dict[str, frozenset[str]] = {
    "diplomacy": DIPLOMACY_KEYWORDS,
    "economy":   ECONOMY_KEYWORDS,
    "disaster":  DISASTER_KEYWORDS,
}


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class HybridDecision:
    prediction: str
    original_prediction: str
    confidence: float
    overridden: bool
    override_reason: str


# ── Internal helpers ──────────────────────────────────────────────────────────

def _weighted_conflict_score(text: str) -> tuple[float, int]:
    raw_scores = score_categories(text, _CONFLICT_CATEGORY_MAP)
    active_cats = {cat: sc for cat, sc in raw_scores.items() if sc > 0}
    indicator_count = len(active_cats)
    if not active_cats:
        return 0.0, 0
    # Peak category score weighted by its importance
    peak_cat = max(active_cats, key=lambda c: active_cats[c] * HDE_CATEGORY_WEIGHTS.get(c, 1.0))
    peak = active_cats[peak_cat] * HDE_CATEGORY_WEIGHTS.get(peak_cat, 1.0)
    # Multi-category boost: each extra active category adds 0.06 (capped at 0.30)
    boost = min(0.30, (indicator_count - 1) * 0.06)
    score = round(min(1.0, peak + boost), 4)
    return score, indicator_count


def _weighted_protest_score(text: str) -> tuple[float, int]:
    raw_scores = score_categories(text, _PROTEST_CATEGORY_MAP)
    score = round(min(1.0, raw_scores.get("protest", 0.0)), 4)
    indicator_count = int(raw_scores.get("protest", 0.0) * HDE_SCORE_CAP)
    return score, indicator_count


def _peace_dampening_score(text: str) -> float:
    raw_scores = score_categories(text, _PEACE_CATEGORY_MAP)
    active = {cat: sc for cat, sc in raw_scores.items() if sc > 0}
    if not active:
        return 0.0
    peak_cat = max(active, key=lambda c: active[c] * HDE_CATEGORY_WEIGHTS.get(c, 1.0))
    peak = active[peak_cat] * HDE_CATEGORY_WEIGHTS.get(peak_cat, 1.0)
    boost = min(0.20, (len(active) - 1) * 0.05)
    return round(min(1.0, peak + boost), 4)


def _min_indicators(confidence: float) -> int:
    if confidence < HDE_LOW_CONFIDENCE_THRESHOLD:
        return HDE_MIN_INDICATORS_LOW
    return HDE_MIN_INDICATORS_MEDIUM


# ── Public decision function ──────────────────────────────────────────────────

def decide(
    text: str,
    ml_prediction: str,
    ml_confidence: float,
) -> HybridDecision:
    # ML is highly confident → always trust it
    if ml_confidence >= HDE_ML_TRUST_THRESHOLD:
        return HybridDecision(
            prediction=ml_prediction,
            original_prediction=ml_prediction,
            confidence=ml_confidence,
            overridden=False,
            override_reason="",
        )

    conflict_score, conflict_indicators = _weighted_conflict_score(text)
    protest_score, protest_indicators = _weighted_protest_score(text)
    peace_score = _peace_dampening_score(text)
    min_ind = _min_indicators(ml_confidence)

    # ── Conflict override check ───────────────────────────────────────────────
    if ml_prediction != "conflict":
        conflict_strong_enough = (
            conflict_score >= HDE_CONFLICT_OVERRIDE_SCORE
            and conflict_indicators >= min_ind
        )
        peace_dampened = (
            ml_prediction == "normal"
            and peace_score >= HDE_DIPLOMACY_DAMPENING_SCORE
            and conflict_score < HDE_CONFLICT_OVERRIDE_SCORE + 0.15
        )
        if conflict_strong_enough and not peace_dampened:
            reason = (
                f"Conflict score {conflict_score:.3f} with {conflict_indicators} "
                f"indicator(s) overrides ML '{ml_prediction}' "
                f"(confidence {ml_confidence:.3f})"
            )
            return HybridDecision(
                prediction="conflict",
                original_prediction=ml_prediction,
                confidence=ml_confidence,
                overridden=True,
                override_reason=reason,
            )

    # ── Protest override check ────────────────────────────────────────────────
    if ml_prediction == "normal":
        protest_strong_enough = (
            protest_score >= HDE_PROTEST_OVERRIDE_SCORE
            and protest_indicators >= min_ind
        )
        if protest_strong_enough:
            reason = (
                f"Protest score {protest_score:.3f} with {protest_indicators} "
                f"indicator(s) overrides ML 'normal' "
                f"(confidence {ml_confidence:.3f})"
            )
            return HybridDecision(
                prediction="protest",
                original_prediction=ml_prediction,
                confidence=ml_confidence,
                overridden=True,
                override_reason=reason,
            )

    return HybridDecision(
        prediction=ml_prediction,
        original_prediction=ml_prediction,
        confidence=ml_confidence,
        overridden=False,
        override_reason="",
    )
