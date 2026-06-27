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
  Event Severity (rule-based)
      |
  Explainable Intelligence (modular keyword mapping)
      |
  Region Extraction (keyword-based)
      |
  Threat Escalation Score (weighted: prediction × confidence × severity)
      |
  Anomaly Detection (threshold-based)
      |
  Trend Analysis (temporal comparison)
      |
  React Dashboard (Vite)
```

---

## Features

### Backend

- Modular FastAPI architecture with separated routes, services, and configuration
- DistilBERT-based event classification (conflict / protest / normal)
- Signal confidence scoring derived from model logits via softmax
- Rule-based event severity classification (LOW / MEDIUM / HIGH / CRITICAL)
- Explainable Intelligence: Modular keyword-based reasoning generation for model predictions
- Confidence- and severity-weighted Threat Escalation Score (TES) per region
- RSS-based live news ingestion (BBC World)
- Keyword-based geographic region extraction (Middle East, South Asia, Europe, USA)
- Threshold-based anomaly detection per region
- In-memory temporal trend analysis per region
- CORS-enabled API with Swagger documentation

### Frontend

- React 19 application built with Vite
- Two-column responsive layout (text analysis + live news dashboard)
- Region cards with TES indicator showing score and risk category label
- Color-coded TES risk categories: Low (green), Moderate (yellow), High (orange), Critical (red)
- Color-coded event classification cards
- Signal confidence displayed as percentage with color-coded progress bar
- Event severity displayed as a color-coded badge with severity bar
- Explainable Intelligence: Collapsible reasoning panel detailing why a prediction was made
- Real-time loading states and error handling

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI |
| NLP Model | DistilBERT (Hugging Face Transformers) |
| ML Runtime | PyTorch |
| News Ingestion | feedparser (RSS) |
| Frontend Framework | React 19 |
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
    "Missile or projectile terminology detected",
    "Aerial strike language identified",
    "Border conflict context found"
  ]
}
```

### GET /news-analysis

Fetch and analyze live news. Returns region-grouped intelligence.

**Response:**
```json
{
  "South Asia": {
    "TES": 1.1340,
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
        ]
      }
    ]
  }
}
```

> TES range is `[0.0, 1.5]`. A single CRITICAL conflict event at full confidence produces `1.0 × 1.0 × 1.5 = 1.5`.

---

## Project Structure

```
AEGIS-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── ml/
│   │   │   └── model_loader.py
│   │   ├── models/
│   │   │   └── schema.py
│   │   ├── services/
│   │   │   ├── anomaly_service.py
│   │   │   ├── explanation_service.py
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
│   │   │   │   └── ExplanationPanel.jsx
│   │   │   ├── InputBox.jsx
│   │   │   ├── MainInterface.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   ├── SeverityBadge.jsx
│   │   │   └── TESBadge.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── App.css
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
