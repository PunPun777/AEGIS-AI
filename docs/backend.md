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
│   │   └── config.py
│   ├── ml/
│   │   ├── __init__.py
│   │   └── model_loader.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schema.py
│   └── services/
│       ├── __init__.py
│       ├── anomaly_service.py
│       ├── explanation_service.py
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

---

## Model Loading

`app/ml/model_loader.py` loads the DistilBERT model and tokenizer from `MODEL_PATH` at import time. The model runs on CPU. Exports module-level `model` and `tokenizer` objects.

---

## Request and Response Schemas

`app/models/schema.py` defines:

- `TextInput`: Pydantic model with a single `text: str` field. Used as the request body for `POST /predict`.
- `PredictionResult`: Pydantic model with `prediction: str`, `confidence: float`, `severity: str`, and `explanation: list[str]` fields. Used as the typed response model for `POST /predict`.

---

## Services

### predictor.py

**Function**: `predict(text: str) -> dict`

Tokenizes input text and runs DistilBERT inference under `torch.no_grad()`. Applies softmax over the raw model logits to produce a probability distribution across all classes. The class with the highest probability is selected; its index is mapped to a label string via `LABEL_MAP`, and its probability value is extracted as the confidence score. Calls `get_severity()` with the resolved prediction label and the original text to produce the severity level. Finally, calls `generate_explanation()` to derive the reasoning string array.

**Returns**:

```python
{
    "prediction": "conflict",   # str
    "confidence": 0.9271,       # float, 0.0–1.0
    "severity": "CRITICAL",     # str
    "explanation": [            # list[str]
        "Military terminology detected"
    ]
}
```

### explanation_service.py

**Function**: `generate_explanation(text: str, prediction: str) -> list[str]`

Implements modular, rule-based reasoning generation. Scans the lowercase text against predefined groups of keywords (e.g., military, protests, economic) categorized by the `prediction` label. Each matching keyword group appends a human-readable analyst sentence to the list. If no keywords match, falls back to a generic explanation string for that class. Keeps inference and keyword logic strictly decoupled.

### severity_service.py

**Function**: `get_severity(prediction: str, text: str) -> str`

Implements rule-based severity assignment. For `"conflict"` predictions, scans the headline text (case-insensitive) against `CRITICAL_KEYWORDS`: `missile`, `airstrike`, `explosion`, `terror`, `invasion`, `war`. Returns `"CRITICAL"` if any keyword is found, `"HIGH"` otherwise. For all other predictions, defers to `SEVERITY_MAP`: `"protest"` → `"MEDIUM"`, `"normal"` → `"LOW"`.

### tes_service.py

**Function**: `calculate_tes(events: list[dict]) -> float`

Computes the Threat Escalation Score as the average of per-event scores, where each event score is:

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
TES = sum(prediction_weight × confidence × severity_multiplier) / number_of_events
```

**TES range**: `[0.0, 1.5]`. A single CRITICAL conflict event at confidence 1.0 produces `1.0 × 1.0 × 1.5 = 1.5`. A normal event with LOW severity at confidence 0.5 produces `0.2 × 0.5 × 0.8 = 0.08`.

**Backward compatibility**: `confidence` falls back to `1.0` and `severity` falls back to `"LOW"` (multiplier `1.0`) if those keys are absent from an event dict.

Returns a float rounded to four decimal places. Function signature unchanged: `list[dict] -> float`.

### news_service.py

**Function**: `fetch_news() -> list[str]`

Parses the configured RSS feed using feedparser. Returns up to `NEWS_LIMIT` article titles as a list of strings.

### region_service.py

**Function**: `get_region(text: str) -> str`

Matches text against keyword lists for four regions: Middle East, South Asia, Europe, USA. Returns the first matching region or "Other" if no match is found. Matching is case-insensitive.

### anomaly_service.py

**Function**: `detect_anomaly(events: list[dict]) -> bool`

Calculates the ratio of high-severity events (conflict + protest) to total events. Returns `True` if the ratio exceeds the threshold of 0.6.

### trend_service.py

**Function**: `get_trend(region: str, current_tes: float) -> str`

Maintains an in-memory dictionary of previous TES values per region. Compares current TES to previous TES and returns "increasing", "decreasing", or "stable". Returns "stable" on first invocation for a region. State resets when the server restarts.

---

## API Routes

`app/api/routes.py` defines two endpoints:

- `POST /predict`: Single text classification returning prediction, confidence, and severity
- `GET /news-analysis`: Live news intelligence analysis with weighted TES per region

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
