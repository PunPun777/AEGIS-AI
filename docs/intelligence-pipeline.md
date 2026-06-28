# Intelligence Pipeline

## Overview

The AEGIS-AI intelligence pipeline transforms raw RSS news data into structured, region-grouped intelligence output. The pipeline executes on each `GET /news-analysis` request.

---

## Pipeline Stages

### 1. News Ingestion

**Service**: `news_service.py`
**Input**: BBC World RSS feed URL
**Output**: List of article title strings (up to 15)

Parses the configured RSS feed using the feedparser library. Extracts article titles as the primary text for analysis.

### 2. NLP Classification

**Service**: `predictor.py`
**Input**: Single text string
**Output**: `{ "prediction": "conflict | protest | normal", "confidence": float, "severity": str, "explanation": list[str] }`

Each article title is individually tokenized and passed through the fine-tuned DistilBERT model. The model outputs raw logits for three classes. Softmax is applied over the logits to produce a normalized probability distribution. The class with the highest probability is selected as the prediction; its probability value is extracted as the confidence score.

**Confidence Derivation**:

```python
probabilities = F.softmax(outputs.logits, dim=-1)
pred_index = probabilities.argmax().item()
confidence = probabilities[0][pred_index].item()
```

### 3. Signal Confidence

**Source**: `predictor.py` (derived within the same inference pass as classification)
**Input**: Softmax probability tensor from stage 2
**Output**: Float in `[0.0, 1.0]`

Confidence is produced as part of the prediction result and propagated through all downstream stages. Every event carries a `confidence` score that is consumed by `tes_service.py`.

### 4. Event Severity

**Service**: `severity_service.py`
**Input**: Prediction label string, original article text string
**Output**: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"`

Rule-based severity assignment:

| Prediction | Base Severity | Escalation Condition | Escalated Severity |
|---|---|---|---|
| `"normal"` | `"LOW"` | N/A | N/A |
| `"protest"` | `"MEDIUM"` | N/A | N/A |
| `"conflict"` | `"HIGH"` | Critical keyword match via `keyword_matcher` | `"CRITICAL"` |

Critical keywords: Handled by `keyword_matcher.has_match()` using `CRITICAL_SEVERITY_TRIGGERS` (covering 200+ terms including missiles, airstrikes, terrorism, and nuclear threats) from `domain_knowledge.py`.

Severity is propagated through all downstream stages. `tes_service.py` consumes the `severity` key to apply the correct multiplier.

### 5. Explainable Intelligence

**Service**: `explanation_service.py`
**Input**: Prediction label string, original article text string
**Output**: List of human-readable explanation strings

Delegates to `keyword_matcher.match_explanation_groups()` to scan the text for predefined keyword groups mapped to the prediction class. Generates reusable explanation sentences (e.g., "Missile or projectile terminology detected"). Uses longest-phrase priority to accurately parse compound expressions like "exchange of fire" without leaking internal rules or heuristics.

### 6. Region Extraction

**Service**: `region_service.py`
**Input**: Single text string
**Output**: Region name string

Performs case-insensitive matching using `REGION_KEYWORDS` from `domain_knowledge.py` covering 8 major regions:

| Region | Example Keywords |
|---|---|
| Middle East | israel, gaza, iran, syria, hezbollah |
| South Asia | india, pakistan, afghanistan, kashmir |
| East Asia | china, taiwan, japan, north korea, south china sea |
| Europe | ukraine, russia, france, nato, kyiv, donbas |
| Africa | nigeria, ethiopia, somalia, sahel |
| Latin America | mexico, colombia, brazil, venezuela, cartels |
| Central Asia | kazakhstan, uzbekistan, azerbaijan |
| USA | united states, washington, pentagon |

Returns `"Other"` if no keywords match. First matching region wins.

### 7. Event Grouping

**Location**: `routes.py` (orchestration logic)

After classification, explanation, and region extraction, events are grouped into a dictionary keyed by region name. Each event stores the article title, prediction label, confidence score, severity level, and explanation array.

```python
{
    "title": "...",
    "prediction": "conflict",
    "confidence": 0.9271,
    "severity": "CRITICAL",
    "explanation": [
        "Military terminology detected"
    ]
}
```

### 8. Threat Escalation Score (TES)

**Service**: `tes_service.py`
**Input**: List of events for a region
**Output**: Dictionary containing `{ tes, risk_score, risk_level }`

Computes the TES as the average of per-event scores. Each event score is the product of three factors:

```
event_score = prediction_weight × confidence × severity_multiplier
TES = sum(event_score) / number_of_events
```

**Prediction weights** (`PREDICTION_WEIGHTS`):

| Prediction | Weight |
|---|---|
| `conflict` | 1.0 |
| `protest` | 0.6 |
| `normal` | 0.2 |

**Severity multipliers** (`SEVERITY_MULTIPLIERS`):

| Severity | Multiplier |
|---|---|
| `LOW` | 0.8 |
| `MEDIUM` | 1.0 |
| `HIGH` | 1.2 |
| `CRITICAL` | 1.5 |

**Worked examples**:

- Single CRITICAL conflict event, confidence 0.98: `1.0 × 0.98 × 1.5 = 1.47`
- Single MEDIUM protest event, confidence 0.88: `0.6 × 0.88 × 1.0 = 0.528`
- Single LOW normal event, confidence 0.83: `0.2 × 0.83 × 0.8 = 0.1328`

Returns a dictionary with the numeric score and a mapped risk level. Backward compatible: `confidence` falls back to `1.0` and `severity` falls back to `"LOW"` if absent.

**Risk category thresholds** (used by frontend `TESCard`):

| TES | Risk Level |
|---|---|
| >= 0.91 | `"CRITICAL"` |
| >= 0.61 | `"HIGH"` |
| >= 0.31 | `"MODERATE"` |
| < 0.31 | `"LOW"` |

### 9. Anomaly Detection

**Service**: `anomaly_service.py`
**Input**: List of events for a region
**Output**: Boolean

Calculates the ratio of high-severity events (conflict + protest) to total events. If the ratio exceeds 0.6 (60%), the region is flagged as anomalous.

### 10. Trend Analysis

**Service**: `trend_service.py`
**Input**: Region name, current TES value
**Output**: `"increasing"`, `"decreasing"`, or `"stable"`

Maintains an in-memory dictionary mapping region names to their previous TES values. On each invocation:

- If no previous value exists (first request): returns `"stable"`
- If current TES > previous TES: returns `"increasing"`
- If current TES < previous TES: returns `"decreasing"`
- If current TES == previous TES: returns `"stable"`

The previous value is updated after each comparison. State is lost on server restart.

### 11. Intelligence Aggregation (Map Endpoint)

**Service**: `map_service.py`
**Input**: Live grouped regions and events
**Output**: List of stripped, flattened region dictionaries

When the `/intelligence-map` endpoint is hit, the pipeline delegates to the standard flow up to Trend Analysis, but instead of returning the full list of raw news events, it strips them down and calculates map-specific metrics: `event_count`, `confidence_average` (mean confidence), and `severity_distribution` (a dictionary tallying how many events fell into each severity category). The array is sorted by `risk_score` descending.

---

## Output Structure

The pipeline produces a JSON object keyed by region:

```json
{
  "Region Name": {
    "TES": 1.2164,
    "risk_score": 1.2164,
    "risk_level": "CRITICAL",
    "anomaly": true,
    "trend": "increasing",
    "events": [
      {
        "title": "Article headline text",
        "prediction": "conflict",
        "confidence": 0.9812,
        "severity": "CRITICAL",
        "explanation": [
          "Military terminology detected"
        ]
      }
    ]
  }
}
```

---

## Pipeline Execution Flow

```
fetch_news()
    |
    v
[article_1, article_2, ..., article_N]
    |
    |--- for each article:
    |       predict(article)     -> { prediction, confidence, severity, explanation }
    |       get_region(article)  -> region
    |       group into: { region: [{ title, prediction, confidence, severity, explanation }] }
    |
    v
{ region: [{ title, prediction, confidence, severity, explanation }] }
    |
    |--- for each region:
    |       calculate_tes(events)
    |           -> get_tes_result() -> { tes, risk_score, risk_level }
    |       detect_anomaly(events)       -> anomaly
    |       get_trend(region, TES)       -> trend
    |
    v
{ region: { TES, risk_score, risk_level, anomaly, trend, events } }
    |
    |--- Branch based on endpoint:
    |
    |--- GET /news-analysis
    |       -> Return direct object structure
    |
    |--- GET /intelligence-map (via map_service.py)
            -> Calculate: confidence_average, severity_distribution, event_count
            -> Strip events array
            -> Format as list sorted by risk_score descending
            -> Return { regions: [...] }
```

---

## Performance Characteristics

- Pipeline runs synchronously per request
- Model inference is the primary bottleneck (CPU-bound, per-article)
- Softmax adds negligible overhead (tensor operation on already-computed logits)
- Severity classification adds negligible overhead (frozenset lookup, no I/O)
- TES weighted calculation is O(n) in the number of events
- RSS fetch adds network latency on each request
- No caching of RSS results or model predictions
- Typical execution: 15 articles processed per request
