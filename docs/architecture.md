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
Event Severity (rule-based)
    |
Explainable Intelligence (modular keyword mapping)
    |
Region Extraction (keyword matching)
    |
Weighted TES Calculation
    |
Anomaly Detection (threshold check)
    |
Trend Analysis (temporal comparison)
    |
React Dashboard (visualization)
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
│   └── config.py         Centralized configuration constants
├── ml/
│   └── model_loader.py   Model and tokenizer initialization
├── models/
│   └── schema.py         Pydantic request/response schemas
└── services/
    ├── predictor.py       NLP inference, confidence scoring, severity assignment
    ├── severity_service.py Rule-based event severity classification
    ├── explanation_service.py Generates human-readable reasoning for predictions
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
Contains all business logic. Each service is a standalone module with a single responsibility. `predictor.py` calls `severity_service.py` and `explanation_service.py` to enrich its output. `tes_service.py` consumes the enriched event dict (including `confidence` and `severity`) to compute the weighted score.

**ML Layer** (`ml/model_loader.py`):
Loads the DistilBERT model and tokenizer at startup. Exports module-level `model` and `tokenizer` objects consumed by the predictor service.

**Configuration Layer** (`core/config.py`):
Stores constants: model path, RSS URL, news limit, label map. All services import configuration from this single source.

**Schema Layer** (`models/schema.py`):
Defines Pydantic models for request validation and response serialization. Includes `TextInput` (request) and `PredictionResult` (response with `prediction`, `confidence`, `severity`, and `explanation`).

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
│   ├── MainInterface.jsx    Primary interface: text input + live news dashboard
│   ├── intelligence/        Explainable Intelligence & TES UI
│   │   ├── ExplanationPanel.jsx
│   │   ├── ExplanationList.jsx
│   │   ├── ExplanationItem.jsx
│   │   ├── RiskBadge.jsx
│   │   ├── RiskMeter.jsx
│   │   └── TESCard.jsx
│   ├── InputBox.jsx         Text input with validation and loading states
│   ├── ResultCard.jsx       Single-text classification result display
│   ├── ConfidenceIndicator.jsx  Reusable confidence percentage and progress bar
│   └── SeverityBadge.jsx    Reusable severity level badge with colored bar
├── services/
│   └── api.js               Axios client (predictText, fetchNewsAnalysis)
└── styles/
    └── App.css              Global design system (dark glassmorphism theme)
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
    │           └── Event Cards
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
    -> DistilBERT inference -> softmax -> get_severity() -> generate_explanation()
    -> { prediction, confidence, severity, explanation }
    -> ResultCard -> SeverityBadge + ConfidenceIndicator + ExplanationPanel
```

### Live News Analysis

```
Button Click -> fetchNewsAnalysis() -> GET /news-analysis
    -> fetch_news() [RSS]
    -> predict() [per article] -> { prediction, confidence, severity, explanation }
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
