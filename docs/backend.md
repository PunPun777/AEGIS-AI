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
│       ├── news_service.py
│       ├── predictor.py
│       ├── region_service.py
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
| `LABEL_MAP` | `{0: "conflict", 1: "normal", 2: "protest"}` | Model output to label mapping |

---

## Model Loading

`app/ml/model_loader.py` loads the DistilBERT model and tokenizer from `MODEL_PATH` at import time. The model runs on CPU. Exports module-level `model` and `tokenizer` objects.

---

## Request Schemas

`app/models/schema.py` defines:

- `TextInput`: Pydantic model with a single `text: str` field.

---

## Services

### predictor.py

**Function**: `predict(text: str) -> str`

Tokenizes input text, runs DistilBERT inference (no gradient), applies argmax to logits, and maps the result to a label string using `LABEL_MAP`.

### news_service.py

**Function**: `fetch_news() -> list[str]`

Parses the configured RSS feed using feedparser. Returns up to `NEWS_LIMIT` article titles as a list of strings.

### region_service.py

**Function**: `get_region(text: str) -> str`

Matches text against keyword lists for four regions: Middle East, South Asia, Europe, USA. Returns the first matching region or "Other" if no match is found. Matching is case-insensitive.

### tes_service.py

**Function**: `calculate_tes(events: list[dict]) -> float`

Computes the Threat Escalation Score as a weighted average of event predictions. Weights: conflict = 1.0, protest = 0.6, normal = 0.2. Returns a float rounded to two decimal places.

### anomaly_service.py

**Function**: `detect_anomaly(events: list[dict]) -> bool`

Calculates the ratio of high-severity events (conflict + protest) to total events. Returns `True` if the ratio exceeds the threshold of 0.6.

### trend_service.py

**Function**: `get_trend(region: str, current_tes: float) -> str`

Maintains an in-memory dictionary of previous TES values per region. Compares current TES to previous TES and returns "increasing", "decreasing", or "stable". Returns "stable" on first invocation for a region. State resets when the server restarts.

---

## API Routes

`app/api/routes.py` defines two endpoints:

- `POST /predict`: Single text classification
- `GET /news-analysis`: Live news intelligence analysis

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
| torch | PyTorch inference runtime |
| feedparser | RSS feed parsing (implicit dependency) |
| pydantic | Request validation (included with FastAPI) |

---

## Deployment (Future)

- Containerization (Docker)
- Cloud deployment (Render / AWS / GCP)
- Model hosting via Hugging Face Hub
