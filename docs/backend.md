# Backend Documentation

## Framework

FastAPI with uvicorn ASGI server.

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── diagnostics.py
│   │   ├── domain_knowledge.py
│   │   └── keyword_matcher.py
│   ├── ml/
│   │   ├── __init__.py
│   │   └── model_loader.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schema.py
│   └── services/
│       ├── __init__.py
│       ├── anomaly_service.py
│       ├── decision_explainer.py
│       ├── explanation_service.py
│       ├── hybrid_decision_service.py
│       ├── map_service.py
│       ├── news_service.py
│       ├── predictor.py
│       ├── region_service.py
│       ├── severity_service.py
│       ├── tes_service.py
│       └── trend_service.py
├── model/               Trained DistilBERT weights and tokenizer
└── requirements.txt
```

---

## Application Entrypoint

`app/main.py` creates the FastAPI instance, registers CORS middleware (allow all origins), and includes the API router.

---

## Configuration

`app/core/config.py` defines:

| Constant | Value | Purpose |
|---|---|---|
| `MODEL_PATH` | `"model"` | Path to trained model directory |
| `RSS_URL` | BBC World RSS feed URL | News ingestion source |
| `NEWS_LIMIT` | `15` | Maximum articles per fetch |
| `LABEL_MAP` | `{0: "conflict", 1: "normal", 2: "protest"}` | Model output index to label mapping |
| `HDE_PREDICTION_BASE_WEIGHT` | `{ "conflict": 1.0, ... }` | Base weight applied to ML confidence |
| `HDE_OVERRIDE_MARGIN` | `0.12` | Margin required to override ML prediction |
| `HDE_CATEGORY_WEIGHTS` | `{ "missile": 1.0, ... }` | Multipliers for domain signal strength |
| `HDE_CONTEXT_WEIGHTS` | `{ "missile": 10, ... }` | Integer weights for dominant context ranking |
| `DEBUG_INTELLIGENCE` | `False` | Enables diagnostic trace output in API responses |

### domain_knowledge.py

**Geopolitical Domain Intelligence Layer**

Acts as the single source of truth for all geopolitical vocabulary. Defines over 21 named `frozenset[str]` categories (e.g., `AIRSTRIKE_KEYWORDS`, `CYBER_KEYWORDS`, `COUP_KEYWORDS`). It also defines composite sets like `CRITICAL_SEVERITY_TRIGGERS` and structures explanation data into groups (e.g., `CONFLICT_EXPLANATION_GROUPS`). Contains expanded regional vocabulary covering 8 major geopolitical zones.

### keyword_matcher.py

**Intelligent Keyword Matcher**

Provides a reusable matching engine for all text-scanning services. Capabilities include:
- **Longest-phrase priority**: Matches "missile barrage" before "missile".
- **Covered-span deduplication**: Prevents double-counting overlapping shorter phrases.
- **Compound phrase support**: Matches multi-word expressions like "exchange of fire".
- **Category Scoring & Confidence**: Can score text across multiple categories to derive signal strength.

Public API includes `has_match()`, `match_phrases()`, `match_explanation_groups()`, and `score_categories()`.

---

## Model Loading

`app/ml/model_loader.py` loads the DistilBERT model and tokenizer from `MODEL_PATH` at import time. The model runs on CPU. Exports module-level `model` and `tokenizer` objects.

---

## Request and Response Schemas

`app/models/schema.py` defines:

- `TextInput`: Pydantic model with a single `text: str` field. Used as the request body for `POST /predict`.
- `PredictionResult`: Pydantic model with `prediction`, `confidence`, `severity`, `explanation`, `original_prediction`, `overridden`, `override_reason`, `matched_categories`, and `matched_keywords`. Used as the typed response model for `POST /predict`.
- `IntelligenceMapResponse`: Response model for the `/intelligence-map` endpoint. Contains a list of `RegionMapEntry` objects, each holding aggregated metrics (`tes`, `risk_level`, `severity_distribution`, etc.) for geographic display.

---

## Services

### predictor.py

**Function**: `predict(text: str) -> dict`

Tokenizes input text and runs DistilBERT inference under `torch.no_grad()`. Applies softmax over the raw model logits to produce a probability distribution across all classes. The class with the highest probability is selected; its index is mapped to a label string via `LABEL_MAP`, and its probability value is extracted as the confidence score. Passes this raw ML prediction to `decide()` in `hybrid_decision_service.py`, which aggregates domain signals and computes the final evidence-based prediction. Calls `get_severity()` with the resolved final prediction label and the original text to produce the severity level. Finally, calls `generate_explanation()` with the `DecisionExplanation` to derive the geopolitically-weighted reasoning string array. Also conditionally attaches a `_diagnostics` object via `build_diagnostics()` if `DEBUG_INTELLIGENCE` is enabled.

**Returns**:

```python
{
    "prediction": "conflict",   # str
    "confidence": 0.6500,       # float, 0.0–1.0
    "severity": "CRITICAL",     # str
    "explanation": [            # list[str]
        "Moderate missile and projectile terminology detected...",
        "Military terminology detected"
    ],
    "original_prediction": "normal",
    "overridden": True,
    "override_reason": "Moderate missile and projectile terminology detected...",
    "dominant_category": "missile",
    "matched_categories": ["missile", "military"],
    "matched_keywords": ["missile strike", "military"],
    "keyword_score": 0.56,
    "override_score": 0.56,
    "category_scores": {"missile": 0.36, "military": 0.20}
}
```

### hybrid_decision_service.py

**Function**: `decide(text: str, ml_prediction: str, ml_confidence: float) -> HybridDecision`

Implements the Evidence-Based Hybrid Decision Engine. The service ALWAYS scans the text across 18 distinct categories (conflict, protest, and peace dampening) regardless of ML confidence. It calculates an `ml_evidence_score` based on base weights and confidence, and a `domain_evidence_score` via the `keyword_matcher`. It compares the scores to determine if an override is warranted. Returns a `HybridDecision` dataclass containing the final prediction, original prediction, override flag, and a rich `DecisionExplanation` containing `dominant_category` and `category_scores`.

### decision_explainer.py

**Function**: `build(...) -> DecisionExplanation`

Produces structured reasoning for every branch of the Hybrid Decision Engine. It determines the `dominant_category` based on predefined geopolitical weighting (`HDE_CONTEXT_WEIGHTS`), dynamically formats analyst-grade contrast sentences, and packages the matched categories, keywords, and numeric scores into a reusable `DecisionExplanation` object consumed by the frontend `DiagnosticsPanel` and `HybridDecisionPanel`.

### explanation_service.py

**Function**: `generate_explanation(text: str, prediction: str) -> list[str]`

Implements modular, rule-based reasoning generation. Delegates to `keyword_matcher.match_explanation_groups()` to scan the text for predefined explanation groups imported from `domain_knowledge.py`. It uses the `dominant_category` from the `DecisionExplanation` to sort and rank explanation sentences, ensuring the most geopolitically significant context appears first and suppresses irrelevant signals. If no groups match, it falls back to a generic explanation string for that class.

### severity_service.py

**Function**: `get_severity(prediction: str, text: str) -> str`

Implements rule-based severity assignment. For `"conflict"` predictions, it calls `keyword_matcher.has_match()` using the `CRITICAL_SEVERITY_TRIGGERS` imported from `domain_knowledge.py`. The trigger set covers hundreds of terms including weapons, terrorism, nuclear threats, and cyber warfare. Returns `"CRITICAL"` if any phrase matches, `"HIGH"` otherwise. For all other predictions, defers to `SEVERITY_MAP`: `"protest"` → `"MEDIUM"`, `"normal"` → `"LOW"`.

### tes_service.py

**Function**: `get_tes_result(events: list[dict]) -> dict`

Computes the Threat Escalation Score by delegating to a private `_compute_score` helper. Each event score is:

```
event_score = prediction_weight × confidence × severity_multiplier
```

**Prediction weights** (`PREDICTION_WEIGHTS`):

| Prediction | Weight |
|---|---|
| `conflict` | 1.0 |
| `protest` | 0.6 |
| `normal` | 0.2 |

**Severity multipliers** (`SEVERITY_MULTIPLIERS`):

| Severity | Multiplier |
|---|---|
| `LOW` | 0.8 |
| `MEDIUM` | 1.0 |
| `HIGH` | 1.2 |
| `CRITICAL` | 1.5 |

**Formula**:

```
score = sum(prediction_weight × confidence × severity_multiplier) / number_of_events
```

Returns a dictionary with three fields: `tes` (the float score), `risk_score` (duplicate of `tes` for frontend clarity), and `risk_level` (mapped from `RISK_THRESHOLDS`).

**Risk Thresholds** (`RISK_THRESHOLDS`):

| Score | Level |
|---|---|
| >= 0.91 | `"CRITICAL"` |
| >= 0.61 | `"HIGH"` |
| >= 0.31 | `"MODERATE"` |
| < 0.31 | `"LOW"` |

**Backward compatibility**: The module still exports `calculate_tes(events: list[dict]) -> float`, which directly returns the float score for legacy callers. `confidence` defaults to `1.0` and `severity` to `"LOW"` if missing.

### news_service.py

**Function**: `fetch_news() -> list[str]`

Parses the configured RSS feed using feedparser. Returns up to `NEWS_LIMIT` article titles as a list of strings.

### region_service.py

**Function**: `get_region(text: str) -> str`

Matches text against comprehensive regional vocabulary imported from `domain_knowledge.py` covering 8 regions (Middle East, South Asia, East Asia, Europe, Africa, Latin America, Central Asia, USA). Returns the first matching region or "Other" if no match is found. Matching is case-insensitive and leverages the expanded domain dictionaries.

### anomaly_service.py

**Function**: `detect_anomaly(events: list[dict]) -> bool`

Calculates the ratio of high-severity events (conflict + protest) to total events. Returns `True` if the ratio exceeds the threshold of 0.6.

### trend_service.py

**Function**: `get_trend(region: str, current_tes: float) -> str`

Maintains an in-memory dictionary of previous TES values per region. Compares current TES to previous TES and returns "increasing", "decreasing", or "stable". Returns "stable" on first invocation for a region. State resets when the server restarts.

### map_service.py

**Function**: `build_intelligence_map() -> list[dict]`

Delegates to `fetch_news()`, classifies all articles, and groups them by region. Uses `tes_service`, `anomaly_service`, and `trend_service` to compute high-level metrics for each region. Strips out raw event lists and constructs a lightweight, aggregated array of geographic data optimized for frontend map visualization. Returns a list sorted by risk score descending.

---

## API Routes

`app/api/routes.py` defines three endpoints:

- `POST /predict`: Single text classification returning prediction, confidence, and severity
- `GET /news-analysis`: Live news intelligence analysis with weighted TES per region
- `GET /intelligence-map`: Aggregated regional intelligence optimized for geographic visualization

See [api.md](api.md) for full endpoint documentation.

---

## Running the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

---

## Dependencies

| Package | Purpose |
|---|---|
| fastapi | Web framework |
| uvicorn | ASGI server |
| transformers | Hugging Face model loading and tokenization |
| torch | PyTorch inference runtime and softmax |
| feedparser | RSS feed parsing |
| pydantic | Request/response validation (included with FastAPI) |

---

## Deployment (Future)

- Containerization (Docker)
- Cloud deployment (Render / AWS / GCP)
- Model hosting via Hugging Face Hub
