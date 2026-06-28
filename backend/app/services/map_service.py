"""
map_service.py
--------------
Phase 6 — Geographic Intelligence Map Service

Aggregates per-region intelligence into a frontend-friendly structure
suitable for map visualisation.  All heavy lifting (prediction, TES,
anomaly, trend) is delegated to the existing services; this module only
assembles the final payload.
"""

from app.services.news_service import fetch_news
from app.services.predictor import predict
from app.services.region_service import get_region
from app.services.tes_service import get_tes_result
from app.services.anomaly_service import detect_anomaly
from app.services.trend_service import get_trend


def _build_severity_distribution(events: list[dict]) -> dict[str, int]:
    """Return a count of events per severity level."""
    distribution: dict[str, int] = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for event in events:
        level = event.get("severity", "LOW")
        distribution[level] = distribution.get(level, 0) + 1
    return distribution


def _compute_confidence_average(events: list[dict]) -> float:
    """Return the mean confidence across all events in a region."""
    if not events:
        return 0.0
    return round(sum(e.get("confidence", 0.0) for e in events) / len(events), 4)


def build_intelligence_map() -> list[dict]:
    """
    Fetch the latest news, run the full analysis pipeline, then return
    one summary dict per detected region — ready to be serialised as JSON.

    Each entry contains:
        region              str
        risk_level          str   ("LOW" | "MODERATE" | "HIGH" | "CRITICAL")
        risk_score          float
        tes                 float
        trend               str   ("stable" | "increasing" | "decreasing")
        anomaly             bool
        event_count         int
        confidence_average  float
        severity_distribution  dict[str, int]
    """
    news_list = fetch_news()

    # ── 1. Classify every article and group by region ───────────────────────
    grouped: dict[str, list[dict]] = {}
    for text in news_list:
        result = predict(text)
        region = get_region(text)
        grouped.setdefault(region, []).append(
            {
                "prediction": result["prediction"],
                "confidence": result["confidence"],
                "severity": result["severity"],
            }
        )

    # ── 2. Aggregate per region ──────────────────────────────────────────────
    map_data: list[dict] = []
    for region, events in grouped.items():
        tes_data = get_tes_result(events)
        anomaly = detect_anomaly(events)
        trend = get_trend(region, tes_data["tes"])

        map_data.append(
            {
                "region": region,
                "risk_level": tes_data["risk_level"],
                "risk_score": tes_data["risk_score"],
                "tes": tes_data["tes"],
                "trend": trend,
                "anomaly": anomaly,
                "event_count": len(events),
                "confidence_average": _compute_confidence_average(events),
                "severity_distribution": _build_severity_distribution(events),
            }
        )

    # ── 3. Sort deterministically: highest risk first ────────────────────────
    map_data.sort(key=lambda r: r["risk_score"], reverse=True)

    return map_data
