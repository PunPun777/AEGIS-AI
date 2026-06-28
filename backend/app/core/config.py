MODEL_PATH = "model"

RSS_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"

NEWS_LIMIT = 15

LABEL_MAP = {
    0: "conflict",
    1: "normal",
    2: "protest"
}

# ── Hybrid Decision Engine ─────────────────────────────────────────────────

# Minimum ML confidence above which the ML prediction is never overridden
HDE_ML_TRUST_THRESHOLD: float = 0.80

# Minimum ML confidence below which keyword signals can freely override
HDE_LOW_CONFIDENCE_THRESHOLD: float = 0.70

# Category score cap — number of distinct phrase matches that produce score 1.0
HDE_SCORE_CAP: int = 5

# Conflict override: score must exceed this to override non-conflict prediction
HDE_CONFLICT_OVERRIDE_SCORE: float = 0.40

# Protest override: score must exceed this to override non-protest prediction
HDE_PROTEST_OVERRIDE_SCORE: float = 0.35

# Diplomacy/peace dampening: if both conflict and these scores are high,
# reduce the chance of overriding to conflict
HDE_DIPLOMACY_DAMPENING_SCORE: float = 0.50

# Minimum indicator count required for an override at medium confidence
HDE_MIN_INDICATORS_MEDIUM: int = 3

# Minimum indicator count required for an override at low confidence
HDE_MIN_INDICATORS_LOW: int = 2

# Category weights applied during scoring (conflict sub-categories)
HDE_CATEGORY_WEIGHTS: dict[str, float] = {
    "missile":    1.0,
    "airstrike":  1.0,
    "military":   0.8,
    "conflict":   0.9,
    "terrorism":  1.0,
    "nuclear":    1.0,
    "cyber":      0.8,
    "insurgency": 0.8,
    "coup":       0.9,
    "weapon":     0.9,
    "shelling":   0.9,
    "naval":      0.8,
    "casualty":   0.7,
    "border":     0.6,
    "protest":    0.9,
    "diplomacy":  0.6,
    "economy":    0.5,
    "disaster":   0.5,
}
