from fastapi import APIRouter
from app.models.schema import TextInput
from app.services.predictor import predict
from app.services.news_service import fetch_news
from app.services.region_service import get_region
from app.services.tes_service import calculate_tes

router = APIRouter()

@router.post("/predict")
def get_prediction(input: TextInput):
    return {"prediction": predict(input.text)}

@router.get("/news-analysis")
def analyze_news():
    news_list = fetch_news()
    grouped: dict[str, list[dict]] = {}
    for text in news_list:
        prediction = predict(text)
        region = get_region(text)
        grouped.setdefault(region, []).append({"title": text, "prediction": prediction})
    return {
        region: {"TES": calculate_tes(events), "events": events}
        for region, events in grouped.items()
    }
