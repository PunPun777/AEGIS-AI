# AEGIS-AI

### Advanced Early Geopolitical Intelligence System

---

## Overview

AEGIS-AI is a predictive intelligence system that identifies early signals of geopolitical instability using AI and open-source data. It ingests live news via RSS, classifies events using a fine-tuned NLP model, derives signal confidence from model logits, assigns an event severity level, generates explainable reasoning for predictions, computes a confidence- and severity-weighted Threat Escalation Score per region, groups events by geographic region, and produces structured intelligence output with anomaly detection and trend analysis.

---

## Architecture

```
RSS Feed (BBC World)
      |
  NLP Classification (DistilBERT)
      |
  Signal Confidence (softmax)
      |
  Hybrid Decision Engine (Evidence Scoring)
      |
  Explainable Intelligence & Severity (via keyword_matcher)
      |
  Region Extraction (via keyword_matcher)
      |
  Geopolitical Domain Intelligence Layer (domain_knowledge)
      |
  Region Extraction (keyword-based)
      |
  Weighted TES Calculation
      |
  Anomaly Detection (threshold-based)
      |
  Trend Analysis (temporal comparison)
      |
  Intelligence Aggregation (/intelligence-map)
      |
  React Dashboard (Vite) + Geographic Map (Leaflet)
```

---

## Features

### Backend

- Modular FastAPI architecture with separated routes, services, and configuration
- DistilBERT-based event classification (conflict / protest / normal)
- Signal confidence scoring derived from model logits via softmax
- Geopolitical Domain Intelligence Layer: Centralized, comprehensive geopolitical vocabulary covering 21+ categories
- Hybrid Decision Engine: Intelligently aggregates ML and domain evidence (weighted category scoring) to decide whether to retain or override predictions, removing previous confidence-first bypass logic.
- Intelligent Keyword Matcher: Reusable matching engine featuring longest-phrase priority, covered-span deduplication, and compound phrase support
- Diagnostics Mode: Built-in developer visibility exposing the internal decision and evidence-scoring process.
- Rule-based event severity classification (LOW / MEDIUM / HIGH / CRITICAL) using domain knowledge
- Explainable Intelligence: Modular reasoning generation for model predictions and hybrid overrides
- Confidence- and severity-weighted Threat Escalation Score (TES) per region
- RSS-based live news ingestion (BBC World)
- Geographic region extraction (Middle East, South Asia, East Asia, Europe, Africa, Latin America, Central Asia, USA)
- Threshold-based anomaly detection per region
- In-memory temporal trend analysis per region
- Dedicated map service serving aggregated regional intelligence (`/intelligence-map`)
- CORS-enabled API with Swagger documentation

### Frontend

- React 19 application built with Vite
- Interactive Geographic Intelligence Map (Leaflet & React-Leaflet) serving as primary dashboard
- Two-column responsive layout (text analysis + live news dashboard)
- Region cards featuring a rich `TESCard` with Threat Escalation Score, Risk Level, and visual Risk Meter
- Interactive Map popups with TES, risk metrics, severity distribution, and average confidence
- Color-coded event classification cards and map regions
- Hybrid Decision Panel: Collapsible UI detailing AI overrides, matched categories, and matched keywords
- Diagnostics Panel: Collapsible developer UI exposing internal ML vs domain evidence scores and decision rationale
- Explainable Intelligence: Collapsible reasoning panel detailing why a prediction was made with geopolitically weighted context
- Real-time loading states, error handling, and map fullscreen controls

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI |
| NLP Model | DistilBERT (Hugging Face Transformers) |
| ML Runtime | PyTorch |
| News Ingestion | feedparser (RSS) |
| Frontend Framework | React 19 |
| Maps Integration | Leaflet / React-Leaflet |
| Build Tool | Vite |
| HTTP Client | Axios |
| Routing | react-router-dom |

---

## API Endpoints

### POST /predict

Classify a single text input.

**Request:**
```json
{
  "text": "Missile strike reported near the capital"
}
```

**Response:**
```json
{
  "prediction": "conflict",
  "confidence": 0.9812,
  "severity": "CRITICAL",
  "explanation": [
    "Prediction retained because ML confidence (98.1%) exceeded the override threshold (80%). Domain signals were not evaluated.",
    "Missile or projectile terminology detected",
    "Aerial strike language identified",
    "Border conflict context found"
  ],
  "original_prediction": "conflict",
  "overridden": false,
  "override_reason": "Prediction retained because ML confidence (98.1%) exceeded the override threshold (80%). Domain signals were not evaluated.",
  "dominant_category": "missile",
  "matched_categories": [],
  "matched_keywords": [],
  "keyword_score": 0.0,
  "override_score": 0.0,
  "category_scores": {}
}
```

> **Note**: Setting `DEBUG_INTELLIGENCE=True` in `config.py` injects a `_diagnostics` block into the response exposing internal evidence scores.

### GET /news-analysis

Fetch and analyze live news. Returns region-grouped intelligence with detailed events.

**Response:**
```json
{
  "South Asia": {
    "TES": 1.1340,
    "risk_score": 1.1340,
    "risk_level": "CRITICAL",
    "anomaly": true,
    "trend": "increasing",
    "events": [
      {
        "title": "Missile strike reported near the capital",
        "prediction": "conflict",
        "confidence": 0.9812,
        "severity": "CRITICAL",
        "explanation": [
          "Missile or projectile terminology detected",
          "Aerial strike language identified"
        ],
        "original_prediction": "conflict",
        "overridden": false,
        "override_reason": "Prediction retained because ML confidence (98.1%) exceeded the override threshold (80%). Domain signals were not evaluated.",
        "dominant_category": "missile",
        "matched_categories": [],
        "matched_keywords": [],
        "keyword_score": 0.0,
        "override_score": 0.0,
        "category_scores": {}
      }
    ]
  }
}
```

> TES range is `[0.0, 1.5]`. A single CRITICAL conflict event at full confidence produces `1.0 × 1.0 × 1.5 = 1.5`.

### GET /intelligence-map

Aggregate intelligence payload for geographic map visualizations, stripping detailed events.

**Response:**
```json
{
  "regions": [
    {
      "region": "South Asia",
      "risk_level": "CRITICAL",
      "risk_score": 1.1340,
      "tes": 1.1340,
      "trend": "increasing",
      "anomaly": true,
      "event_count": 1,
      "confidence_average": 0.9812,
      "severity_distribution": {
        "LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 1
      }
    }
  ]
}
```

---

## Project Structure

```
AEGIS-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── domain_knowledge.py
│   │   │   └── keyword_matcher.py
│   │   ├── ml/
│   │   │   └── model_loader.py
│   │   ├── models/
│   │   │   └── schema.py
│   │   ├── services/
│   │   │   ├── anomaly_service.py
│   │   │   ├── decision_explainer.py
│   │   │   ├── explanation_service.py
│   │   │   ├── hybrid_decision_service.py
│   │   │   ├── map_service.py
│   │   │   ├── news_service.py
│   │   │   ├── predictor.py
│   │   │   ├── region_service.py
│   │   │   ├── severity_service.py
│   │   │   ├── tes_service.py
│   │   │   └── trend_service.py
│   │   └── main.py
│   ├── model/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConfidenceIndicator.jsx
│   │   │   ├── intelligence/
│   │   │   │   ├── ExplanationItem.jsx
│   │   │   │   ├── ExplanationList.jsx
│   │   │   │   ├── ExplanationPanel.jsx
│   │   │   │   ├── HybridDecisionPanel.jsx
│   │   │   │   ├── RiskBadge.jsx
│   │   │   │   ├── RiskMeter.jsx
│   │   │   │   └── TESCard.jsx
│   │   │   ├── map/
│   │   │   │   ├── IntelligenceMap.jsx
│   │   │   │   ├── MapControls.jsx
│   │   │   │   ├── RegionPopup.jsx
│   │   │   │   └── RiskLegend.jsx
│   │   │   ├── EventCard.jsx
│   │   │   ├── InputBox.jsx
│   │   │   ├── MainInterface.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── SeverityBadge.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── App.css
│   │   │   └── map.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── docs/
```

---

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Development server: http://localhost:5173

---

## Model

- Architecture: DistilBERT (fine-tuned)
- Training data: AG News with heuristic relabeling
- Classes: conflict, protest, normal
- Confidence: softmax probability of the predicted class
- Storage: local `backend/model/` directory (Git LFS)

---

## Limitations

- Model trained on AG News, not real geopolitical datasets
- Region extraction is keyword-based, not NER-based
- Trend analysis uses in-memory storage (resets on server restart)
- Severity classification is rule-based, not learned
- Confidence scores are not calibrated
- TES severity multiplier list is fixed and does not adapt
- No persistent database
- No authentication or rate limiting

---

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for the full phased roadmap.

---

## Author

### Punarvi M U

---

## Vision

AEGIS-AI aims to evolve into a real-time geopolitical early warning system for governments, analysts, and organizations.
