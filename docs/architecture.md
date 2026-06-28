# System Architecture

## Intelligence Pipeline

The system operates as a multi-stage intelligence pipeline:

```
RSS Feed (BBC World)
    |
NLP Classification (DistilBERT)
    |
Signal Confidence (softmax)
    |
  Hybrid Decision Engine (Evidence Scoring)
    |
  Event Severity (using Domain Knowledge & Keyword Matcher)
      |
  Explainable Intelligence (using Domain Knowledge & Keyword Matcher)
      |
  Region Extraction (using Domain Knowledge & Keyword Matcher)
      |
Weighted TES Calculation
    |
Anomaly Detection (threshold check)
    |
Trend Analysis (temporal comparison)
    |
Intelligence Aggregation (/intelligence-map)
    |
React Dashboard (Vite) + Geographic Map (Leaflet)
```

---

## Backend Architecture

The backend follows a modular layered design:

```
app/
├── main.py               Application entrypoint, CORS, router registration
├── api/
│   └── routes.py         HTTP endpoint definitions
├── core/
│   ├── config.py             Centralized configuration constants
│   ├── diagnostics.py        Internal decision pipeline visibility 
│   ├── domain_knowledge.py   Geopolitical vocabulary and categories
│   └── keyword_matcher.py    Reusable keyword matching engine
├── ml/
│   └── model_loader.py   Model and tokenizer initialization
├── models/
│   └── schema.py         Pydantic request/response schemas
└── services/
    ├── predictor.py       NLP inference, confidence scoring, severity assignment
    ├── hybrid_decision_service.py Aggregates ML and domain evidence to determine final prediction
    ├── decision_explainer.py Generates geopolitically-weighted reasoning for hybrid decisions
    ├── severity_service.py Rule-based event severity classification
    ├── explanation_service.py Generates human-readable reasoning for predictions
    ├── map_service.py     Aggregates regional intelligence for map visualizations
    ├── news_service.py    RSS feed ingestion
    ├── region_service.py  Geographic region extraction
    ├── tes_service.py     Confidence- and severity-weighted TES calculation
    ├── anomaly_service.py Anomaly detection
    └── trend_service.py   Temporal trend tracking
```

### Layer Responsibilities

**API Layer** (`api/routes.py`):
Defines HTTP endpoints. Orchestrates calls to the services layer. Contains no business logic.

**Services Layer** (`services/`):
Contains all business logic. Each service is a standalone module with a single responsibility. `predictor.py` passes ML output to `hybrid_decision_service.py` which evaluates domain signals and calls `decision_explainer.py`. It then calls `severity_service.py` and `explanation_service.py` to enrich its output. `tes_service.py` consumes the enriched event dict (including `confidence` and `severity`) to compute the weighted score. `map_service.py` aggregates regional intelligence for the map endpoints.

**ML Layer** (`ml/model_loader.py`):
Loads the DistilBERT model and tokenizer at startup. Exports module-level `model` and `tokenizer` objects consumed by the predictor service.

**Core Layer** (`core/`):
- `config.py`: Stores constants: model path, RSS URL, news limit, label map. All services import configuration from this single source.
- `domain_knowledge.py`: Single source of truth for geopolitical vocabulary, covering 21+ semantic categories and extended regions.
- `keyword_matcher.py`: Stateless engine for matching phrases. Implements longest-phrase priority, covered-span deduplication, and category scoring. Used by multiple downstream services.

**Schema Layer** (`models/schema.py`):
Defines Pydantic models for request validation and response serialization. Includes `TextInput` (request) and `PredictionResult` (response with `prediction`, `confidence`, `severity`, and `explanation`), as well as `IntelligenceMapResponse` and `RegionMapEntry`.

---

## Frontend Architecture

The frontend is a React 19 single-page application built with Vite:

```
src/
├── App.jsx                  Router setup (BrowserRouter)
├── main.jsx                 React DOM render entrypoint
├── pages/
│   └── Home.jsx             Page shell: header, hero, footer
├── components/
│   ├── MainInterface.jsx    Primary interface: intelligence map + text analysis + live news
│   ├── map/                 Geographic map components (Leaflet)
│   │   ├── IntelligenceMap.jsx
│   │   ├── RegionPopup.jsx
│   │   ├── RiskLegend.jsx
│   ├── intelligence/        Explainable Intelligence & TES UI
│   │   ├── ExplanationPanel.jsx
│   │   ├── ExplanationList.jsx
│   │   ├── ExplanationItem.jsx
│   │   ├── HybridDecisionPanel.jsx
│   │   ├── DiagnosticsPanel.jsx
│   │   ├── RiskBadge.jsx
│   │   ├── MainInterface.jsx    Primary dashboard: text analysis + live news
│   ├── EventCard.jsx        Reusable event card displaying intelligence metrics
│   ├── InputBox.jsx         Text input with validation and loading states
│   ├── ResultCard.jsx       Single-text classification result display
│   ├── ConfidenceIndicator.jsx  Reusable confidence percentage and progress bar
│   └── SeverityBadge.jsx    Reusable severity level badge with colored bar
├── services/
│   └── api.js               Axios client (predictText, fetchNewsAnalysis, fetchIntelligenceMap)
└── styles/
    ├── App.css              Global design system (dark glassmorphism theme)
    └── map.css              Intelligence map styling
```

### Component Hierarchy

```
App
└── Home
    ├── Header (app-header)
    ├── Hero (hero section)
    ├── MainInterface
    │   ├── InputBox
    │   ├── ResultCard
    │   │   ├── SeverityBadge
    │   │   ├── ConfidenceIndicator
    │   │   └── ExplanationPanel
    │   └── Live News Dashboard
    │       └── Region Card (per region)
    │           ├── Anomaly Badge
    │           ├── TESCard
    │           │   ├── RiskBadge
    │           │   └── RiskMeter
    │           ├── Trend Badge
    │           └── Event Cards (EventCard)
    │               ├── HybridDecisionPanel
    │               ├── DiagnosticsPanel
    │               ├── SeverityBadge
    │               ├── ConfidenceIndicator
    │               └── ExplanationPanel
    └── Footer (app-footer)
```

---

## Data Flow

### Single Text Analysis

```
User Input -> InputBox -> predictText(text) -> POST /predict -> predictor.predict()
    -> DistilBERT inference -> softmax
    -> decide() [Hybrid Decision Engine]
    -> get_severity() -> generate_explanation()
    -> { prediction, original_prediction, overridden, confidence, severity, explanation, ... }
    -> ResultCard -> SeverityBadge + ConfidenceIndicator + ExplanationPanel + HybridDecisionPanel
```

### Live News Analysis

```
Button Click -> fetchNewsAnalysis() -> GET /news-analysis
    -> fetch_news() [RSS]
    -> predict() [per article] -> { prediction, overridden, confidence, severity, explanation, ... }
    -> get_region() [per article]
    -> group by region -> { region: [{ title, prediction, confidence, severity, explanation }] }
    -> calculate_tes() [per region]
        -> get_tes_result() -> { tes, risk_score, risk_level }
    -> detect_anomaly() [per region]
    -> get_trend() [per region]
    -> JSON response -> Region Cards
        -> TESCard (score + risk level + risk meter)
        -> Event Cards -> SeverityBadge + ConfidenceIndicator + ExplanationPanel
```

---

## Cross-Cutting Concerns

**CORS**: Enabled via FastAPI middleware with permissive defaults (allow all origins). Intended for local development.

**State Management**: React `useState` hooks. No external state library.

**Error Handling**: Frontend catches API errors and displays messages via InputBox. Backend relies on FastAPI default error responses.
