from __future__ import annotations

from app.core.domain_knowledge import (
    CONFLICT_EXPLANATION_GROUPS,
    PROTEST_EXPLANATION_GROUPS,
    NORMAL_EXPLANATION_GROUPS,
    DIPLOMACY_KEYWORDS,
    CEASEFIRE_KEYWORDS,
    PEACE_KEYWORDS,
    ECONOMY_KEYWORDS,
    ELECTION_KEYWORDS,
    DISASTER_KEYWORDS,
    REFUGEE_KEYWORDS,
    SANCTION_KEYWORDS,
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
from app.core.config import HDE_CONTEXT_WEIGHTS
from app.core.keyword_matcher import match_explanation_groups, score_categories
from app.services.decision_explainer import DecisionExplanation, _CATEGORY_LABELS

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

# Full category maps used for scoring within explanation_service independently
# of what the HDE computed (covers all prediction types).
_ALL_CATEGORY_MAP: dict[str, frozenset[str]] = {
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
    "protest":    PROTEST_KEYWORDS,
    "diplomacy":  DIPLOMACY_KEYWORDS,
    "economy":    ECONOMY_KEYWORDS,
    "disaster":   DISASTER_KEYWORDS,
}

# Maps each explanation-group sentence prefix to its category key.
_SENTENCE_CATEGORY_MAP: dict[str, str] = {
    "Missile or projectile":              "missile",
    "Aerial strike":                      "airstrike",
    "Heavy weapons and shelling":         "shelling",
    "Terrorism-related":                  "terrorism",
    "Nuclear or WMD":                     "nuclear",
    "Cyberattack or cyber warfare":       "cyber",
    "Military deployment or force":       "military",
    "Naval confrontation":                "naval",
    "Weapons or armament":                "weapon",
    "Insurgency or guerrilla":            "insurgency",
    "Coup or governmental overthrow":     "coup",
    "Casualty or human loss":             "casualty",
    "Active conflict or warfare":         "conflict",
    "Border conflict or territorial":     "border",
    "Sanctions or economic pressure":     "economy",
    "Protest activity":                   "protest",
    "Public demonstration":               "protest",
    "Organized march":                    "protest",
    "Civil unrest or riot":               "protest",
    "Security force crackdown":           "protest",
    "Industrial or civil action":         "protest",
    "Non-violent resistance":             "protest",
    "Activist or organized movement":     "protest",
    "Grievance and demand":               "protest",
    "Uprising or political opposition":   "protest",
    "Diplomatic agreement":               "diplomacy",
    "Diplomatic engagement":              "diplomacy",
    "Ceasefire or peace process":         "diplomacy",
    "Peace or reconciliation":            "diplomacy",
    "Economic context":                   "economy",
    "Positive economic development":      "economy",
    "Humanitarian or disaster":           "disaster",
    "Refugee or displacement":            "disaster",
    "Political process or electoral":     "diplomacy",
    "Diplomatic process":                 "diplomacy",
    "Sanction or economic pressure":      "economy",
    "Cultural event or celebration":      "diplomacy",
    "Education or research":              "diplomacy",
}


def _sentence_category(sentence: str) -> str:
    for prefix, cat in _SENTENCE_CATEGORY_MAP.items():
        if sentence.startswith(prefix):
            return cat
    return ""


def _context_weight(cat: str) -> int:
    return HDE_CONTEXT_WEIGHTS.get(cat, 1)


def _resolve_dominant(
    text: str,
    decision_explanation: DecisionExplanation | None,
    prediction: str,
) -> str:
    if decision_explanation and decision_explanation.dominant_category:
        return decision_explanation.dominant_category

    raw = score_categories(text, _ALL_CATEGORY_MAP)
    active = {c: s for c, s in raw.items() if s > 0}
    if not active:
        return ""

    return max(active, key=lambda c: active[c] * _context_weight(c))


def generate_explanation(
    text: str,
    prediction: str,
    decision_explanation: DecisionExplanation | None = None,
) -> list[str]:
    groups = _EXPLANATION_GROUPS.get(prediction, [])
    all_sentences = match_explanation_groups(text, groups)

    dominant = _resolve_dominant(text, decision_explanation, prediction)

    if dominant and all_sentences:
        def _rank(s: str) -> tuple[int, int]:
            cat = _sentence_category(s)
            is_dominant = int(cat == dominant)
            return (-is_dominant, -_context_weight(cat))

        ranked = sorted(all_sentences, key=_rank)

        dominant_sentences = [s for s in ranked if _sentence_category(s) == dominant]
        supporting = [
            s for s in ranked
            if _sentence_category(s) != dominant
            and _context_weight(_sentence_category(s)) >= _context_weight(dominant) - 3
        ]
        sentences = (dominant_sentences[:1] + supporting[:2]) or ranked[:3]
    else:
        sentences = all_sentences[:3]

    if not sentences:
        sentences = [_FALLBACK_EXPLANATIONS.get(prediction, "Classification based on model output")]

    if decision_explanation and decision_explanation.decision_reason:
        reason = decision_explanation.decision_reason
        if reason not in sentences:
            sentences = [reason] + sentences

    return sentences
