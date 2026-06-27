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
| `LABEL_MAP` | `{0: "conflict", 1: "normal", 2: "protest"}` | Model output index to label mapping |

---

## Model Loading

`app/ml/model_loader.py` loads the DistilBERT model and tokenizer from `MODEL_PATH` at import time. The model runs on CPU. Exports module-level `model` and `tokenizer` objects.

---

## Request and Response Schemas

`app/models/schema.py` defines:

- `TextInput`: Pydantic model with a single `text: str` field. Used as the request body for `POST /predict`.
- `PredictionResult`: Pydantic model with `prediction: str` and `confidence: float` fields. Used as the typed response model for `POST /predict`.

---

## Services

### predictor.py

**Function**: `predict(text: str) -> dict`

Tokenizes input text and runs DistilBERT inference under `torch.no_grad()`. Applies softmax over the raw model logits to produce a probability distribution across all classes. The class with the highest probability is selected; its index is mapped to a label string via `LABEL_MAP`, and its probability value is extracted as the confidence score.

**Confidence Derivation**:

```python
probabilities = F.softmax(outputs.logits, dim=-1)
pred_index = probabilities.argmax().item()
confidence = probabilities[0][pred_index].item()
```

Confidence is a float in the range `[0.0, 1.0]`, representing the model's normalized probability for the predicted class. It is rounded to four decimal places. Formatting as a percentage is the responsibility of the consuming layer (frontend).

**Returns**:

```python
{
    "prediction": "conflict",   # str
    "confidence": 0.9271        # float, 0.0–1.0
}
```

### news_service.py

**Function**: `fetch_news() -> list[str]`

Parses the configured RSS feed using feedparser. Returns up to `NEWS_LIMIT` article titles as a list of strings.

### region_service.py

**Function**: `get_region(text: str) -> str`

Matches text against keyword lists for four regions: Middle East, South Asia, Europe, USA. Returns the first matching region or "Other" if no match is found. Matching is case-insensitive.

### tes_service.py

**Function**: `calculate_tes(events: list[dict]) -> float`

Computes the Threat Escalation Score as a weighted average of event predictions. Each event dict must contain a `prediction` key. Weights: conflict = 1.0, protest = 0.6, normal = 0.2. Returns a float rounded to two decimal places.

### anomaly_service.py

**Function**: `detect_anomaly(events: list[dict]) -> bool`

Calculates the ratio of high-severity events (conflict + protest) to total events. Each event dict must contain a `prediction` key. Returns `True` if the ratio exceeds the threshold of 0.6.

### trend_service.py

**Function**: `get_trend(region: str, current_tes: float) -> str`

Maintains an in-memory dictionary of previous TES values per region. Compares current TES to previous TES and returns "increasing", "decreasing", or "stable". Returns "stable" on first invocation for a region. State resets when the server restarts.

---

## API Routes

`app/api/routes.py` defines two endpoints:

- `POST /predict`: Single text classification returning prediction and confidence
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
| torch | PyTorch inference runtime and softmax |
| feedparser | RSS feed parsing |
| pydantic | Request/response validation (included with FastAPI) |

---

## Deployment (Future)

- Containerization (Docker)
- Cloud deployment (Render / AWS / GCP)
- Model hosting via Hugging Face Hub
