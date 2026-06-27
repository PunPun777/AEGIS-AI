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

- Threat Escalation Score (TES) per region (simple prediction-weight average)
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

## Phase 5.4 — Completed

- TES formula upgraded to incorporate prediction weight, signal confidence, and severity multiplier
- `tes_service.py` updated with `PREDICTION_WEIGHTS` and `SEVERITY_MULTIPLIERS` constants
- New formula: `TES = avg(prediction_weight × confidence × severity_multiplier)`
- TES range extended from `[0.0, 1.0]` to `[0.0, 1.5]`
- TES precision increased from 2 decimal places to 4
- Backward-compatible: `confidence` defaults to `1.0`, `severity` defaults to `"LOW"` if absent
- `TESBadge` reusable React component displaying score and risk category label
- Four risk categories derived from TES thresholds: Low (< 0.4), Moderate (0.4–0.69), High (0.7–0.99), Critical (≥ 1.0)
- Color-coded TES display: green (Low), yellow (Moderate), orange (High), red (Critical)
- Replaced hardcoded TES inline markup in `MainInterface.jsx` with `TESBadge` component

---

## Phase 5.5 — Completed

- Explainable Intelligence: modular, rule-based reasoning generation explaining model decisions
- Created `explanation_service.py` to decouple keyword/heuristics logic from model inference
- Mapped explicit keyword clusters to human-readable explanation strings per prediction class
- Integrated `explanation: list[str]` into the prediction pipeline and API responses
- Created reusable React UI components (`ExplanationPanel.jsx`, `ExplanationList.jsx`, `ExplanationItem.jsx`)
- Upgraded intelligence dashboard to display collapsible reasoning sections per event without layout shift

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
