import torch
from app.ml.model_loader import model, tokenizer
from app.core.config import LABEL_MAP

def predict(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    pred = outputs.logits.argmax().item()
    return LABEL_MAP[pred]
