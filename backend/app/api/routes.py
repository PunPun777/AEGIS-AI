from fastapi import APIRouter
from app.models.schema import TextInput, PredictionResult
from app.services.predictor import predict
from app.services.news_service import fetch_news
from app.services.region_service import get_region
from app.services.tes_service import calculate_tes, get_tes_result
from app.services.anomaly_service import detect_anomaly
from app.services.trend_service import get_trend

router = APIRouter()


@router.post("/predict", response_model=PredictionResult)
def get_prediction(input: TextInput):
    return predict(input.text)


@router.get("/news-analysis")
def analyze_news():
    news_list = fetch_news()
    grouped: dict[str, list[dict]] = {}

    for text in news_list:
        result = predict(text)
        region = get_region(text)
        grouped.setdefault(region, []).append({
            "title": text,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "explanation": result["explanation"],
        })

    output = {}
    for region, events in grouped.items():
        tes_data = get_tes_result(events)
        anomaly = detect_anomaly(events)
        trend = get_trend(region, tes_data["tes"])
        output[region] = {
            "TES": tes_data["tes"],
            "risk_score": tes_data["risk_score"],
            "risk_level": tes_data["risk_level"],
            "anomaly": anomaly,
            "trend": trend,
            "events": events,
        }

    return output
