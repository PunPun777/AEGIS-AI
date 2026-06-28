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
- API exposes `tes`, `risk_score`, and `risk_level` natively from the backend
- Four risk categories defined in backend thresholds: LOW (< 0.31), MODERATE (0.31–0.60), HIGH (0.61–0.90), CRITICAL (≥ 0.91)
- Replaced legacy `TESBadge` with a rich composite `TESCard` containing `RiskBadge` and `RiskMeter` visual components
- Fully synchronized repository documentation with API and UI updates

---

## Phase 5.5 — Completed

- Explainable Intelligence: modular, rule-based reasoning generation explaining model decisions
- Created `explanation_service.py` to decouple keyword/heuristics logic from model inference
- Mapped explicit keyword clusters to human-readable explanation strings per prediction class
- Integrated `explanation: list[str]` into the prediction pipeline and API responses
- Created reusable React UI components (`ExplanationPanel.jsx`, `ExplanationList.jsx`, `ExplanationItem.jsx`)
- Upgraded intelligence dashboard to display collapsible reasoning sections per event without layout shift

---

## Phase 6 — Completed

- Interactive geographic visualization (Leaflet.js & React-Leaflet)
- Map-based region display with color-coded risk overlays
- Geographic Intelligence Map API endpoint (`/intelligence-map`) for aggregated data
- Map popups containing TES, risk levels, and severity distribution
- Map dashboard layout with responsive dual-pane structure

---

## Phase 6.5 — Completed

- Geopolitical Domain Intelligence Layer (`domain_knowledge.py`)
- Centralized vocabulary covering 21+ categories (conflict, protest, nuclear, cyber, etc.)
- Extended region extraction covering 8 major geopolitical zones
- Intelligent Keyword Matcher (`keyword_matcher.py`) with longest-phrase priority, compound matching, and category scoring
- Refactored `severity_service.py` and `explanation_service.py` to use centralized vocabulary and matcher
- Prepared shared intelligence architecture for future Multi-source OSINT and NER integration

---

## Phase 7 — Planned

- Multi-source OSINT ingestion (GDELT, ACLED, NewsAPI)
- Named Entity Recognition for region and actor extraction
- Alert system for anomaly notifications
- Persistent storage for historical trend data

---

## Phase 8 — Planned

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
