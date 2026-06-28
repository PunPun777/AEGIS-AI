import torch
import torch.nn.functional as F
from app.ml.model_loader import model, tokenizer
import app.core.config as _cfg
from app.core.diagnostics import build_diagnostics, diagnostics_to_dict
from app.services.severity_service import get_severity
from app.services.explanation_service import generate_explanation
from app.services.hybrid_decision_service import decide


def predict(text: str) -> dict:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = F.softmax(outputs.logits, dim=-1)
    pred_index = probabilities.argmax().item()
    ml_confidence = probabilities[0][pred_index].item()
    ml_prediction = _cfg.LABEL_MAP[pred_index]

    decision = decide(text, ml_prediction, ml_confidence)
    expl = decision.explanation

    result = {
        "prediction":          decision.prediction,
        "confidence":          round(decision.confidence, 4),
        "severity":            get_severity(decision.prediction, text),
        "explanation":         generate_explanation(text, decision.prediction, expl),
        "original_prediction": decision.original_prediction,
        "overridden":          decision.overridden,
        "override_reason":     decision.override_reason,
        "dominant_category":   expl.dominant_category,
        "matched_categories":  expl.matched_categories,
        "matched_keywords":    expl.matched_keywords,
        "keyword_score":       expl.keyword_score,
        "override_score":      expl.override_score,
        "category_scores":     expl.category_scores,
    }

    diag = build_diagnostics(
        ml_prediction=ml_prediction,
        ml_confidence=ml_confidence,
        decision_prediction=decision.prediction,
        overridden=decision.overridden,
        override_reason=decision.override_reason,
        matched_keywords=expl.matched_keywords,
        matched_categories=expl.matched_categories,
        category_scores=expl.category_scores,
        dominant_category=expl.dominant_category,
        keyword_score=expl.keyword_score,
    )
    if diag is not None:
        result["_diagnostics"] = diagnostics_to_dict(diag)

    return result
