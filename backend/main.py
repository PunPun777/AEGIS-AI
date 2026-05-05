from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from fastapi.middleware.cors import CORSMiddleware
import feedparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

device = torch.device("cpu")
model.to(device)

class TextInput(BaseModel):
    text: str

def fetch_news():
    url = "https://feeds.bbci.co.uk/news/world/rss.xml"
    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:15]: 
        articles.append(entry.title)

    return articles

def predict(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    pred = outputs.logits.argmax().item()

    label_map = {
        0: "conflict",
        1: "normal",
        2: "protest"
    }

    return label_map[pred]

@app.post("/predict")
def get_prediction(input: TextInput):
    return {"prediction": predict(input.text)}

@app.get("/news-analysis")
def analyze_news():
    news_list = fetch_news()

    results = []

    for text in news_list:
        prediction = predict(text)
        results.append({
            "title": text,
            "prediction": prediction
        })

    return results