import torch
import torch.nn.functional as F
from app.ml.model_loader import model, tokenizer
from app.core.config import LABEL_MAP


def predict(text: str) -> dict:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = F.softmax(outputs.logits, dim=-1)
    pred_index = probabilities.argmax().item()
    confidence = probabilities[0][pred_index].item()

    return {
        "prediction": LABEL_MAP[pred_index],
        "confidence": round(confidence, 4),
    }
