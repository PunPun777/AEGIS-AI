# AEGIS-AI

### Advanced Early Geopolitical Intelligence System

---

## Overview

AEGIS-AI is a predictive intelligence system that identifies early signals of geopolitical instability using AI and open-source data. It ingests live news via RSS, classifies events using a fine-tuned NLP model, groups them by geographic region, and produces structured intelligence output with threat scoring, anomaly detection, and trend analysis.

---

## Architecture

```
RSS Feed (BBC World)
      |
  NLP Classification (DistilBERT)
      |
  Region Extraction (keyword-based)
      |
  Threat Escalation Score (TES)
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
- RSS-based live news ingestion (BBC World)
- Keyword-based geographic region extraction (Middle East, South Asia, Europe, USA)
- Threat Escalation Score (TES) calculation per region
- Threshold-based anomaly detection per region
- In-memory temporal trend analysis per region
- CORS-enabled API with Swagger documentation

### Frontend

- React 19 application built with Vite
- Two-column responsive layout (text analysis + live news dashboard)
- Region cards with TES, anomaly, and trend indicators
- Color-coded event classification cards
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
  "text": "Mass protests erupted in the capital"
}
```

**Response:**
```json
{
  "prediction": "protest"
}
```

### GET /news-analysis

Fetch and analyze live news. Returns region-grouped intelligence.

**Response:**
```json
{
  "South Asia": {
    "TES": 0.72,
    "anomaly": true,
    "trend": "increasing",
    "events": [
      {
        "title": "...",
        "prediction": "conflict"
      }
    ]
  }
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
│   │   │   └── config.py
│   │   ├── ml/
│   │   │   └── model_loader.py
│   │   ├── models/
│   │   │   └── schema.py
│   │   ├── services/
│   │   │   ├── anomaly_service.py
│   │   │   ├── news_service.py
│   │   │   ├── predictor.py
│   │   │   ├── region_service.py
│   │   │   ├── tes_service.py
│   │   │   └── trend_service.py
│   │   └── main.py
│   ├── model/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── InputBox.jsx
│   │   │   ├── MainInterface.jsx
│   │   │   └── ResultCard.jsx
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
- Storage: local `backend/model/` directory (Git LFS)

---

## Limitations

- Model trained on AG News, not real geopolitical datasets
- Region extraction is keyword-based, not NER-based
- Trend analysis uses in-memory storage (resets on server restart)
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
