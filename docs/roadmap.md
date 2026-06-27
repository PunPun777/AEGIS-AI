# Roadmap

## Phase 1 — Completed

- DistilBERT model training and fine-tuning
- FastAPI backend with prediction API
- Local model inference system

---

## Phase 2 — Completed

- React frontend (Vite)
- Axios-based API integration
- Text input with classification result display
- Responsive layout with dark glassmorphism design

---

## Phase 3 — Completed

- RSS-based live news ingestion (BBC World via feedparser)
- Keyword-based geographic region extraction
- Region-grouped intelligence output

---

## Phase 4 — Completed

- Threat Escalation Score (TES) per region
- Threshold-based anomaly detection per region
- In-memory temporal trend analysis per region
- Live intelligence dashboard with region cards, TES badges, anomaly indicators, and trend display

---

## Phase 5.1 — Completed

- Signal confidence scoring derived from model logits via softmax
- `POST /predict` response extended with `confidence` float field
- `GET /news-analysis` events extended with `confidence` float field
- `PredictionResult` Pydantic response model added to schema layer
- `ConfidenceIndicator` reusable React component
- Confidence displayed in `ResultCard` and every live news event card
- Color-coded confidence bar: green (≥ 90%), yellow (70–89%), red (< 70%)

---

## Phase 5.2 — Completed

- Rule-based event severity classification (LOW / MEDIUM / HIGH / CRITICAL)
- `severity_service.py` implementing keyword-escalation logic for conflict events
- `POST /predict` response extended with `severity` string field
- `GET /news-analysis` events extended with `severity` string field
- `PredictionResult` Pydantic schema updated with `severity: str`
- `SeverityBadge` reusable React component
- Severity displayed alongside confidence in `ResultCard` and every live news event card
- Color-coded severity bar: green (LOW), yellow (MEDIUM), orange (HIGH), red (CRITICAL)

---

## Phase 5.3 — Planned

- Interactive geographic visualization (Leaflet.js)
- Map-based region display with risk overlays
- Alert system for anomaly notifications

---

## Phase 6 — Planned

- Multi-source OSINT ingestion (GDELT, ACLED, NewsAPI)
- Named Entity Recognition for region and actor extraction
- Persistent storage for historical trend data

---

## Phase 7 — Planned

- Model hosting via Hugging Face Hub
- Containerization (Docker)
- Cloud deployment (Render / AWS / GCP)
- Authentication and rate limiting
- Scalable production architecture

---

## Final Goal

A full-stack geopolitical intelligence platform capable of:

- Real-time instability prediction
- Multi-source data fusion
- Geographic risk visualization
- Decision support for analysts and organizations
