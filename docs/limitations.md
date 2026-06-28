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
- Confidence scores are not calibrated; softmax probabilities from a heuristically-labeled model tend to skew toward high confidence regardless of true certainty

---

## Severity Classification Limitations

- Severity is rule-based, relying on keyword matches rather than being learned from data
- A `conflict` event without any matched critical keywords defaults to `HIGH` even if the underlying headline describes a severe incident using novel vocabulary
- Severity does not factor in confidence: a low-confidence `conflict` prediction escalates severity identically to a high-confidence one
- `protest` events are always `MEDIUM` regardless of scale, duration, or accompanying violence

---

## Region Extraction Limitations

- Region extraction relies on the `keyword_matcher` scanning the `domain_knowledge` vocabulary, not Named Entity Recognition (NER)
- Articles matching no keywords in the domain dictionary are grouped under "Other"
- Cannot detect multiple regions within a single article

---

## Intelligence Scoring Limitations

- TES is a simple weighted average, not a calibrated risk metric
- TES weighting is not adjusted by event confidence; a low-confidence conflict prediction carries the same TES weight as a high-confidence one
- TES weighting is not adjusted by event severity; a CRITICAL event carries the same TES weight as a HIGH event
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
- Confidence calibration (temperature scaling) has not been applied
- Severity classification has not been evaluated against a labeled severity dataset

---

## Mitigation Plan

- Train on real geopolitical datasets (GDELT, ACLED event data)
- Apply confidence calibration (temperature scaling, Platt scaling)
- Replace rule-based severity with a learned severity classifier trained on labeled event data
- Incorporate confidence and severity weighting into TES calculation
- Replace keyword-based region extraction with NER models (e.g., spaCy, specialized transformer)
- Implement persistent storage for trend history
- Add adaptive anomaly thresholds
- Add authentication and rate limiting for production deployment
