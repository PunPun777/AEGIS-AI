from fastapi import APIRouter
from app.models.schema import TextInput
from app.services.predictor import predict
from app.services.news_service import fetch_news

router = APIRouter()

@router.post("/predict")
def get_prediction(input: TextInput):
    return {"prediction": predict(input.text)}

@router.get("/news-analysis")
def analyze_news():
    news_list = fetch_news()
    results = []
    for text in news_list:
        prediction = predict(text)
        results.append({"title": text, "prediction": prediction})
    return results
