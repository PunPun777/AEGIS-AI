MODEL_PATH = "model"

RSS_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"

NEWS_LIMIT = 15

LABEL_MAP = {
    0: "conflict",
    1: "normal",
    2: "protest"
}

# ── Hybrid Decision Engine ─────────────────────────────────────────────────

# Base weight multiplied by ML confidence to produce the ML evidence score.
# Reflects how much inherent domain signal each ML class already implies.
HDE_PREDICTION_BASE_WEIGHT: dict[str, float] = {
    "conflict": 1.0,
    "protest":  0.7,
    "normal":   0.25,   # reduced from 0.4 — compensates for model over-confidence on Normal
}

# Domain score must exceed the ML evidence score by at least this margin
# to trigger an override. Prevents weak domain signals from beating
# a confident ML prediction.
HDE_OVERRIDE_MARGIN: float = 0.06         # reduced from 0.12 — allows domain signals to override sooner

# When ML confidence is below this value the margin requirement is relaxed,
# allowing weaker domain signals to override an uncertain ML result.
HDE_LOW_CONFIDENCE_THRESHOLD: float = 0.70
HDE_OVERRIDE_MARGIN_LOW: float = 0.02     # reduced from 0.04 — relaxed further for low-confidence ML predictions

# Absolute minimum domain score below which overrides are never triggered
# regardless of the ML evidence comparison.
HDE_CONFLICT_DOMAIN_FLOOR: float = 0.15   # reduced from 0.20 — allows single-hit conflict signals to qualify
HDE_PROTEST_DOMAIN_FLOOR: float = 0.12   # reduced from 0.16 — symmetrically lowers protest override floor

# Category score cap — number of distinct phrase matches that produce score 1.0
HDE_SCORE_CAP: int = 5

# Peace/diplomacy dampening: when peace_score exceeds conflict_score by this
# ratio, a valid conflict override is suppressed.
HDE_DIPLOMACY_DAMPENING_SCORE: float = 0.45
HDE_PEACE_CONFLICT_RATIO: float = 0.65

# Category weights applied during domain scoring
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

# Integer geopolitical context weights used by the contextual explanation engine.
# Determines which context is dominant when multiple category groups match.
HDE_CONTEXT_WEIGHTS: dict[str, int] = {
    "missile":    10,
    "airstrike":  10,
    "terrorism":  10,
    "nuclear":    10,
    "military":   8,
    "shelling":   8,
    "conflict":   8,
    "insurgency": 7,
    "coup":       7,
    "weapon":     7,
    "naval":      6,
    "cyber":      6,
    "casualty":   6,
    "border":     5,
    "protest":    9,
    "diplomacy":  3,
    "economy":    2,
    "disaster":   2,
}

# Minimum weighted-score lead the dominant context must hold over the
# second-highest context for the contrast sentence to be included.
HDE_DOMINANT_CONTRAST_THRESHOLD: int = 4

# ── Diagnostics ────────────────────────────────────────────────────────────

DEBUG_INTELLIGENCE: bool = False
