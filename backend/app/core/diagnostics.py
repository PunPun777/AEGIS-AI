from __future__ import annotations

from dataclasses import dataclass, field

import app.core.config as _cfg


@dataclass
class IntelligenceDiagnostics:
    ml_prediction: str
    ml_confidence: float
    ml_evidence_score: float
    matched_keywords: list[str]
    matched_categories: list[str]
    category_scores: dict[str, float]
    dominant_category: str
    domain_evidence_score: float
    override_applied: bool
    override_reason: str
    final_prediction: str
    decision: str


def build_diagnostics(
    ml_prediction: str,
    ml_confidence: float,
    decision_prediction: str,
    overridden: bool,
    override_reason: str,
    matched_keywords: list[str],
    matched_categories: list[str],
    category_scores: dict[str, float],
    dominant_category: str,
    keyword_score: float,
) -> IntelligenceDiagnostics | None:
    if not _cfg.DEBUG_INTELLIGENCE:
        return None

    ml_evidence_score = round(
        ml_confidence * _cfg.HDE_PREDICTION_BASE_WEIGHT.get(ml_prediction, 0.5), 4
    )

    if overridden:
        decision = "DOMAIN_OVERRIDE"
    elif keyword_score > 0:
        decision = "ML_RETAINED_WITH_DOMAIN_SIGNALS"
    else:
        decision = "ML_ACCEPTED"

    return IntelligenceDiagnostics(
        ml_prediction=ml_prediction,
        ml_confidence=round(ml_confidence, 4),
        ml_evidence_score=ml_evidence_score,
        matched_keywords=matched_keywords,
        matched_categories=matched_categories,
        category_scores=category_scores,
        dominant_category=dominant_category,
        domain_evidence_score=round(keyword_score, 4),
        override_applied=overridden,
        override_reason=override_reason,
        final_prediction=decision_prediction,
        decision=decision,
    )


def diagnostics_to_dict(d: IntelligenceDiagnostics | None) -> dict | None:
    if d is None:
        return None
    return {
        "ml_prediction":       d.ml_prediction,
        "ml_confidence":       d.ml_confidence,
        "ml_evidence_score":   d.ml_evidence_score,
        "matched_keywords":    d.matched_keywords,
        "matched_categories":  d.matched_categories,
        "category_scores":     d.category_scores,
        "dominant_category":   d.dominant_category,
        "domain_evidence_score": d.domain_evidence_score,
        "override_applied":    d.override_applied,
        "override_reason":     d.override_reason,
        "final_prediction":    d.final_prediction,
        "decision":            d.decision,
    }
