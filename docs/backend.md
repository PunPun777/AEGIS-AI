# Backend Documentation

## Framework

- FastAPI

---

## Responsibilities

- Load trained model
- Handle API requests
- Perform inference
- Return predictions

---

## File Structure

backend/
├── main.py
├── model/
├── requirements.txt

---

## Key Components

### Model Loading

- Loads tokenizer and model from local directory
- Runs on CPU for inference

---

### Prediction Function

- Tokenizes input
- Runs model inference
- Maps output to label

---

### API Layer

- Exposes `/predict` endpoint
- Accepts JSON input
- Returns prediction response

---

## Execution

Run server:

uvicorn main:app --reload

---

## Local Testing

Access Swagger UI:

http://127.0.0.1:8000/docs

---

## Deployment (Future)

- Render / AWS / GCP
- Containerization (Docker)
- Model hosting via Hugging Face
