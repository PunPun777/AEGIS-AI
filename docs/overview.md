# AEGIS-AI Overview

## Project Vision

AEGIS-AI (Advanced Early Geopolitical Intelligence System) is designed to address a key limitation in modern intelligence systems: their reactive nature.

Traditional systems detect and respond to events after they occur. AEGIS-AI introduces a predictive approach that identifies early warning signals of geopolitical instability using artificial intelligence and open-source intelligence (OSINT).

---

## Problem Context

Signals of geopolitical instability exist across multiple sources:

- News articles
- Protest reports
- Political statements
- Conflict databases

However:

- Data is fragmented across platforms
- Analysts manually interpret signals
- No unified predictive system exists

This leads to:

- Delayed responses
- Missed escalation patterns
- Reactive decision-making

---

## Core Idea

AEGIS-AI transforms:

```
Raw Text -> Structured Signals -> Predictive Insight
```

Instead of asking:

> "What has already happened?"

It answers:

> "Where is instability likely to escalate next?"

---

## Current Scope

The current implementation includes:

- Event classification using a fine-tuned DistilBERT model
- Live news ingestion via RSS (BBC World)
- Geographic region extraction
- Threat Escalation Score (TES) per region
- Anomaly detection per region
- Temporal trend analysis per region
- FastAPI backend with modular service architecture
- React frontend with an interactive intelligence dashboard

---

## Future Vision

AEGIS-AI aims to evolve into a full intelligence platform with:

- Multi-source OSINT ingestion (GDELT, ACLED, NewsAPI)
- Named Entity Recognition (NER) for region and actor extraction
- Interactive geographic visualization (Leaflet.js)
- Persistent storage and historical analysis
- Explainable AI signals
- Cloud deployment and model hosting
