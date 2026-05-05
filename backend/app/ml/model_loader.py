import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.core.config import MODEL_PATH

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    device = torch.device("cpu")
    model.to(device)
    return model, tokenizer

model, tokenizer = load_model()
