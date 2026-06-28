from __future__ import annotations

from dataclasses import dataclass

from app.core.config import (
    HDE_PREDICTION_BASE_WEIGHT,
    HDE_OVERRIDE_MARGIN,
    HDE_LOW_CONFIDENCE_THRESHOLD,
    HDE_OVERRIDE_MARGIN_LOW,
    HDE_CONFLICT_DOMAIN_FLOOR,
    HDE_PROTEST_DOMAIN_FLOOR,
    HDE_SCORE_CAP,
    HDE_DIPLOMACY_DAMPENING_SCORE,
    HDE_PEACE_CONFLICT_RATIO,
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
from app.services.decision_explainer import DecisionExplanation, build as build_explanation


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
    explanation: DecisionExplanation


# ── Evidence scoring ──────────────────────────────────────────────────────────

def _ml_evidence_score(ml_prediction: str, ml_confidence: float) -> float:
    base = HDE_PREDICTION_BASE_WEIGHT.get(ml_prediction, 0.5)
    return round(ml_confidence * base, 4)


def _conflict_domain_score(text: str) -> tuple[float, int, list[str]]:
    raw_scores = score_categories(text, _CONFLICT_CATEGORY_MAP)
    active_cats = {cat: sc for cat, sc in raw_scores.items() if sc > 0}
    indicator_count = len(active_cats)
    if not active_cats:
        return 0.0, 0, []
    peak_cat = max(active_cats, key=lambda c: active_cats[c] * HDE_CATEGORY_WEIGHTS.get(c, 1.0))
    peak = active_cats[peak_cat] * HDE_CATEGORY_WEIGHTS.get(peak_cat, 1.0)
    boost = min(0.30, (indicator_count - 1) * 0.06)
    score = round(min(1.0, peak + boost), 4)
    return score, indicator_count, list(active_cats.keys())


def _protest_domain_score(text: str) -> tuple[float, int, list[str]]:
    raw_scores = score_categories(text, _PROTEST_CATEGORY_MAP)
    score = round(min(1.0, raw_scores.get("protest", 0.0)), 4)
    indicator_count = int(raw_scores.get("protest", 0.0) * HDE_SCORE_CAP)
    keywords = match_phrases(text, PROTEST_KEYWORDS)
    return score, indicator_count, keywords


def _peace_score(text: str) -> float:
    raw_scores = score_categories(text, _PEACE_CATEGORY_MAP)
    active = {cat: sc for cat, sc in raw_scores.items() if sc > 0}
    if not active:
        return 0.0
    peak_cat = max(active, key=lambda c: active[c] * HDE_CATEGORY_WEIGHTS.get(c, 1.0))
    peak = active[peak_cat] * HDE_CATEGORY_WEIGHTS.get(peak_cat, 1.0)
    boost = min(0.20, (len(active) - 1) * 0.05)
    return round(min(1.0, peak + boost), 4)


def _required_margin(ml_confidence: float) -> float:
    if ml_confidence < HDE_LOW_CONFIDENCE_THRESHOLD:
        return HDE_OVERRIDE_MARGIN_LOW
    return HDE_OVERRIDE_MARGIN


def _peace_dampens(conflict_score: float, peace: float) -> bool:
    if peace < HDE_DIPLOMACY_DAMPENING_SCORE:
        return False
    if conflict_score <= 0:
        return True
    return (peace / conflict_score) >= HDE_PEACE_CONFLICT_RATIO


# ── Public decision function ──────────────────────────────────────────────────

def decide(
    text: str,
    ml_prediction: str,
    ml_confidence: float,
) -> HybridDecision:
    ml_score = _ml_evidence_score(ml_prediction, ml_confidence)

    conflict_score, conflict_indicators, conflict_cats = _conflict_domain_score(text)
    protest_score, protest_indicators, protest_kws = _protest_domain_score(text)
    peace = _peace_score(text)
    margin = _required_margin(ml_confidence)

    # ── Conflict domain evidence check ────────────────────────────────────────
    if ml_prediction != "conflict":
        conflict_beats_ml = (
            conflict_score >= HDE_CONFLICT_DOMAIN_FLOOR
            and conflict_score > ml_score + margin
        )
        dampened = _peace_dampens(conflict_score, peace)

        if conflict_beats_ml and not dampened:
            expl = build_explanation(
                text, ml_prediction, ml_confidence,
                outcome="conflict_override",
                conflict_score=conflict_score,
                ml_score=ml_score,
                conflict_categories=conflict_cats,
                conflict_indicators=conflict_indicators,
                conflict_category_map=_CONFLICT_CATEGORY_MAP,
            )
            return HybridDecision(
                prediction="conflict",
                original_prediction=ml_prediction,
                confidence=ml_confidence,
                overridden=True,
                override_reason=expl.decision_reason,
                explanation=expl,
            )

        if conflict_beats_ml and dampened:
            expl = build_explanation(
                text, ml_prediction, ml_confidence,
                outcome="peace_dampened",
                conflict_score=conflict_score,
                ml_score=ml_score,
                conflict_categories=conflict_cats,
                peace_score=peace,
                conflict_category_map=_CONFLICT_CATEGORY_MAP,
            )
            return HybridDecision(
                prediction=ml_prediction,
                original_prediction=ml_prediction,
                confidence=ml_confidence,
                overridden=False,
                override_reason=expl.decision_reason,
                explanation=expl,
            )

    # ── Protest domain evidence check ─────────────────────────────────────────
    if ml_prediction != "protest":
        protest_beats_ml = (
            protest_score >= HDE_PROTEST_DOMAIN_FLOOR
            and protest_score > ml_score + margin
        )
        if protest_beats_ml:
            expl = build_explanation(
                text, ml_prediction, ml_confidence,
                outcome="protest_override",
                protest_score=protest_score,
                ml_score=ml_score,
                protest_keywords=protest_kws,
                protest_indicators=protest_indicators,
            )
            return HybridDecision(
                prediction="protest",
                original_prediction=ml_prediction,
                confidence=ml_confidence,
                overridden=True,
                override_reason=expl.decision_reason,
                explanation=expl,
            )

    expl = build_explanation(
        text, ml_prediction, ml_confidence,
        outcome="kept",
        conflict_score=conflict_score,
        ml_score=ml_score,
        conflict_categories=conflict_cats,
        peace_score=peace,
    )
    return HybridDecision(
        prediction=ml_prediction,
        original_prediction=ml_prediction,
        confidence=ml_confidence,
        overridden=False,
        override_reason=expl.decision_reason,
        explanation=expl,
    )
