from pydantic import BaseModel


class TextInput(BaseModel):
    text: str


class PredictionResult(BaseModel):
    prediction: str
    confidence: float
