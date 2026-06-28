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

- Domain Intelligence Engine (`domain_knowledge.py`)
- Geopolitical keyword analysis
- Centralized vocabulary covering 21+ categories
- Rule-based domain scoring and intelligent keyword matcher

---

## Phase 5.6 — Completed

- Hybrid Intelligence Decision Engine (`hybrid_decision_service.py`)
- Confidence-aware decision logic completely replacing confidence-first bypass logic
- Domain vs ML comparison via weighted category scoring
- Explainable hybrid reasoning dynamically sorting analysis reasoning by dominant category
- Diagnostics mode (`DEBUG_INTELLIGENCE`) exposing ML vs Domain internal evidence scores
- Diagnostics Developer Panel added to frontend
- Decision stabilization

---

## Phase 5.7 — Intelligence Model V2 (Active)

**Motivation**: Testing demonstrated that the Hybrid Decision Engine functions correctly. However, the original DistilBERT model frequently predicts the "normal" class with extremely high confidence for many geopolitical headlines. The limitation is now the trained model rather than the backend architecture.

- Expanded geopolitical dataset
- Improved dataset balancing
- Richer geopolitical labels
- Improved preprocessing
- Better evaluation metrics
- Precision / Recall / F1 evaluation
- Confusion Matrix
- Retrained DistilBERT
- Improved conflict recognition
- Better hybrid decision support

---

## Phase 6 — Completed

- Interactive geographic visualization (Leaflet.js & React-Leaflet)
- Map-based region display with color-coded risk overlays
- Geographic Intelligence Map API endpoint (`/intelligence-map`) for aggregated data
- Map popups containing TES, risk levels, and severity distribution
- Map dashboard layout with responsive dual-pane structure

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
