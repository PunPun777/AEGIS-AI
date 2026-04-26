# 🛡️ AEGIS-AI

### Advanced Early Geopolitical Intelligence System

---

## 🚀 Overview

AEGIS-AI is a predictive intelligence system designed to identify early signals of geopolitical instability using AI and open-source data.

Unlike traditional systems that react **after events occur**, AEGIS-AI focuses on:

> 🔍 **Predicting instability before escalation**

---

## 🧠 Core Idea

Transform:

```
Raw Text → NLP Processing → Classification → Risk Signals
```

Instead of asking:

> “What happened?”

AEGIS-AI answers:

> “What is likely to escalate next?”

---

## 🏗️ Current Implementation (Phase 1)

This repository currently includes:

- ✅ Event Classification Model (DistilBERT)
- ✅ FastAPI Backend
- ✅ Prediction API

---

## 🧪 Model Capabilities

The model classifies geopolitical text into:

| Label       | Meaning                         |
| ----------- | ------------------------------- |
| 🔴 Conflict | War, violence, military actions |
| 🟠 Protest  | Demonstrations, riots           |
| 🟢 Normal   | Neutral events                  |

---

## ⚙️ Tech Stack

- Python
- FastAPI
- Transformers (Hugging Face)
- PyTorch
- Git LFS (for model storage)

---

## 📡 API Endpoint

### POST `/predict`

#### Request

```json
{
  "text": "Mass protests erupted in the capital"
}
```

#### Response

```json
{
  "prediction": "protest"
}
```

---

## 🏃 Running the Backend

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Start server

```
cd backend
uvicorn main:app --reload
```

### 3. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```
backend/
│
├── main.py
├── model/
├── requirements.txt
├── .gitignore
```

---

## ⚠️ Notes

- Model is stored using Git LFS due to size constraints
- Current model is trained on labeled news data (AG News + heuristics)
- Accuracy may not reflect real-world generalization

---

## 🚀 Future Roadmap

- 🌍 Integrate real-time OSINT (GDELT, NewsAPI)
- 📊 Risk scoring engine (TES)
- 🗺️ Map-based visualization (Leaflet.js)
- 🤖 Explainable AI signals
- ☁️ Model hosting via Hugging Face

---

## 👩‍💻 Author

### Punarvi M U
---

## ⭐ Vision

AEGIS-AI aims to evolve into:

> A real-time geopolitical early warning system for governments, analysts, and organizations.
