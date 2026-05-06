from fastapi import APIRouter
from app.models.schema import TextInput
from app.services.predictor import predict
from app.services.news_service import fetch_news
from app.services.region_service import get_region
from app.services.tes_service import calculate_tes
from app.services.anomaly_service import detect_anomaly
from app.services.trend_service import get_trend

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

    result = {}
    for region, events in grouped.items():
        tes = calculate_tes(events)
        anomaly = detect_anomaly(events)
        trend = get_trend(region, tes)
        result[region] = {
            "TES": tes,
            "anomaly": anomaly,
            "trend": trend,
            "events": events,
        }
    return result
