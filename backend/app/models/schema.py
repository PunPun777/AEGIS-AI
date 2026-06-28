from pydantic import BaseModel


class TextInput(BaseModel):
    text: str


class PredictionResult(BaseModel):
    prediction: str
    confidence: float
    severity: str
    explanation: list[str]


class RegionMapEntry(BaseModel):
    region: str
    risk_level: str
    risk_score: float
    tes: float
    trend: str
    anomaly: bool
    event_count: int
    confidence_average: float
    severity_distribution: dict[str, int]


class IntelligenceMapResponse(BaseModel):
    regions: list[RegionMapEntry]
