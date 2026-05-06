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
**Output**: Classification label (`"conflict"`, `"protest"`, or `"normal"`)

Each article title is individually tokenized and passed through the fine-tuned DistilBERT model. The model outputs logits for three classes; the highest-scoring class is selected via argmax and mapped to a label string.

### 3. Region Extraction

**Service**: `region_service.py`
**Input**: Single text string
**Output**: Region name string

Performs case-insensitive keyword matching against predefined keyword lists for four regions:

| Region | Example Keywords |
|---|---|
| Middle East | israel, palestine, gaza, iran, iraq, syria |
| South Asia | india, pakistan, afghanistan, kashmir |
| Europe | ukraine, russia, france, nato, kyiv |
| USA | united states, washington, congress, pentagon |

Returns `"Other"` if no keywords match. First matching region wins.

### 4. Event Grouping

**Location**: `routes.py` (orchestration logic)

After classification and region extraction, events are grouped into a dictionary keyed by region name. Each event stores the article title and its prediction label.

### 5. Threat Escalation Score (TES)

**Service**: `tes_service.py`
**Input**: List of events for a region
**Output**: Float score (0.0 - 1.0)

Computes a weighted average of event predictions:

| Prediction | Weight |
|---|---|
| conflict | 1.0 |
| protest | 0.6 |
| normal | 0.2 |

Formula: `TES = sum(weight per event) / number of events`

**Interpretation**:
- TES > 0.7: High threat (red)
- TES >= 0.4: Moderate threat (orange)
- TES < 0.4: Low threat (green)

### 6. Anomaly Detection

**Service**: `anomaly_service.py`
**Input**: List of events for a region
**Output**: Boolean

Calculates the ratio of high-severity events (conflict + protest) to total events. If the ratio exceeds 0.6 (60%), the region is flagged as anomalous.

### 7. Trend Analysis

**Service**: `trend_service.py`
**Input**: Region name, current TES value
**Output**: `"increasing"`, `"decreasing"`, or `"stable"`

Maintains an in-memory dictionary mapping region names to their previous TES values. On each invocation:

- If no previous value exists (first request): returns `"stable"`
- If current TES > previous TES: returns `"increasing"`
- If current TES < previous TES: returns `"decreasing"`
- If current TES == previous TES: returns `"stable"`

The previous value is updated after each comparison. State is lost on server restart.

---

## Output Structure

The pipeline produces a JSON object keyed by region:

```json
{
  "Region Name": {
    "TES": 0.72,
    "anomaly": true,
    "trend": "increasing",
    "events": [
      {
        "title": "Article headline text",
        "prediction": "conflict"
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
    |       predict(article)  ->  prediction
    |       get_region(article)  ->  region
    |       group into: { region: [events] }
    |
    v
{ region: [events] }
    |
    |--- for each region:
    |       calculate_tes(events)  ->  TES
    |       detect_anomaly(events)  ->  anomaly
    |       get_trend(region, TES)  ->  trend
    |
    v
{ region: { TES, anomaly, trend, events } }
```

---

## Performance Characteristics

- Pipeline runs synchronously per request
- Model inference is the primary bottleneck (CPU-bound, per-article)
- RSS fetch adds network latency on each request
- No caching of RSS results or model predictions
- Typical execution: 15 articles processed per request
