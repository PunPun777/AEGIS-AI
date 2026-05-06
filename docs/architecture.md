# System Architecture

## Intelligence Pipeline

The system operates as a multi-stage intelligence pipeline:

```
RSS Feed (BBC World)
    |
NLP Classification (DistilBERT)
    |
Region Extraction (keyword matching)
    |
TES Calculation (weighted scoring)
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
├── main.py              Application entrypoint, CORS, router registration
├── api/
│   └── routes.py        HTTP endpoint definitions
├── core/
│   └── config.py        Centralized configuration constants
├── ml/
│   └── model_loader.py  Model and tokenizer initialization
├── models/
│   └── schema.py        Pydantic request/response schemas
└── services/
    ├── predictor.py      NLP inference abstraction
    ├── news_service.py   RSS feed ingestion
    ├── region_service.py Geographic region extraction
    ├── tes_service.py    Threat Escalation Score calculation
    ├── anomaly_service.py Anomaly detection
    └── trend_service.py  Temporal trend tracking
```

### Layer Responsibilities

**API Layer** (`api/routes.py`):
Defines HTTP endpoints. Orchestrates calls to the services layer. Contains no business logic.

**Services Layer** (`services/`):
Contains all business logic. Each service is a standalone module with a single responsibility. Services do not depend on each other.

**ML Layer** (`ml/model_loader.py`):
Loads the DistilBERT model and tokenizer at startup. Exports module-level `model` and `tokenizer` objects consumed by the predictor service.

**Configuration Layer** (`core/config.py`):
Stores constants: model path, RSS URL, news limit, label map. All services import configuration from this single source.

**Schema Layer** (`models/schema.py`):
Defines Pydantic models for request validation.

---

## Frontend Architecture

The frontend is a React 19 single-page application built with Vite:

```
src/
├── App.jsx              Router setup (BrowserRouter)
├── main.jsx             React DOM render entrypoint
├── pages/
│   └── Home.jsx         Page shell: header, hero, footer
├── components/
│   ├── MainInterface.jsx Primary interface: text input + live news dashboard
│   ├── InputBox.jsx      Text input with validation and loading states
│   └── ResultCard.jsx    Single-text classification result display
├── services/
│   └── api.js            Axios client (predictText, fetchNewsAnalysis)
└── styles/
    └── App.css           Global design system (dark glassmorphism theme)
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
    │   └── Live News Dashboard
    │       └── Region Card (per region)
    │           ├── Anomaly Badge
    │           ├── TES Badge
    │           ├── Trend Badge
    │           └── Event Cards
    └── Footer (app-footer)
```

---

## Data Flow

### Single Text Analysis

```
User Input -> InputBox -> predictText(text) -> POST /predict -> predictor.predict()
    -> DistilBERT inference -> label -> ResultCard
```

### Live News Analysis

```
Button Click -> fetchNewsAnalysis() -> GET /news-analysis
    -> fetch_news() [RSS]
    -> predict() [per article]
    -> get_region() [per article]
    -> group by region
    -> calculate_tes() [per region]
    -> detect_anomaly() [per region]
    -> get_trend() [per region]
    -> JSON response -> Region Cards
```

---

## Cross-Cutting Concerns

**CORS**: Enabled via FastAPI middleware with permissive defaults (allow all origins). Intended for local development.

**State Management**: React `useState` hooks. No external state library.

**Error Handling**: Frontend catches API errors and displays messages via InputBox. Backend relies on FastAPI default error responses.
