import torch
import torch.nn.functional as F
from app.ml.model_loader import model, tokenizer
from app.core.config import LABEL_MAP
from app.services.severity_service import get_severity
from app.services.explanation_service import generate_explanation


def predict(text: str) -> dict:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = F.softmax(outputs.logits, dim=-1)
    pred_index = probabilities.argmax().item()
    confidence = probabilities[0][pred_index].item()
    prediction = LABEL_MAP[pred_index]

    return {
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "severity": get_severity(prediction, text),
        "explanation": generate_explanation(text, prediction),
    }
