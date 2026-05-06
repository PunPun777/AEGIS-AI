# Limitations

## Data Limitations

- Uses AG News dataset (not domain-specific geopolitical data)
- Labels generated using keyword heuristics, not expert annotation
- RSS ingestion limited to a single source (BBC World)
- Only article titles are analyzed, not full article bodies

---

## Model Limitations

- Keyword dependency in classification
- Weak contextual understanding for nuanced geopolitical language
- Struggles with edge cases and ambiguous text
- No confidence score exposed in the API response

---

## Region Extraction Limitations

- Keyword-based matching, not Named Entity Recognition
- Limited to four predefined regions (Middle East, South Asia, Europe, USA)
- Articles matching no keywords are grouped under "Other"
- Cannot detect multiple regions within a single article

---

## Intelligence Scoring Limitations

- TES is a simple weighted average, not a calibrated risk metric
- Anomaly detection uses a fixed threshold (0.6), not adaptive
- Trend analysis uses in-memory storage that resets on server restart
- Trend only compares current vs. previous invocation, not a time series

---

## Deployment Limitations

- Model stored via Git LFS
- No containerization
- No cloud deployment
- No authentication or rate limiting
- CORS configured with permissive defaults (allow all origins)

---

## Evaluation Limitations

- High accuracy (~97-99%) likely inflated due to heuristic labeling
- Not evaluated against real geopolitical ground truth

---

## Mitigation Plan

- Train on real geopolitical datasets (GDELT, ACLED event data)
- Replace keyword region extraction with NER
- Implement persistent storage for trend history
- Add adaptive anomaly thresholds
- Introduce confidence scoring
- Add authentication and rate limiting for production deployment
