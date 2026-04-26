# System Architecture

## High-Level Pipeline

The system is designed as a multi-stage intelligence pipeline:

Data → NLP Processing → Classification → Risk Signals → Visualization

---

## Current Architecture (Phase 1)

Client → FastAPI Backend → ML Model → Prediction → Response

---

## Components

### 1. Data Layer (Future)

Planned sources:

- GDELT
- ACLED
- NewsAPI
- OpenStreetMap

---

### 2. NLP Layer

Processes unstructured text into structured signals:

- Tokenization
- Text encoding
- Context extraction

---

### 3. Classification Layer

Uses a transformer model to classify events into:

- Conflict
- Protest
- Normal

---

### 4. Backend Layer

Handles:

- Model loading
- Inference
- API communication

---

### 5. Visualization Layer (Future)

Planned features:

- Interactive map
- Region-based risk scores
- Alert system

---

## Future Architecture

OSINT Sources
↓
NLP + Entity Recognition
↓
Anomaly Detection
↓
Threat Escalation Score (TES)
↓
Frontend Dashboard
