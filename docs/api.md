# API Documentation

## Base URL

```
http://127.0.0.1:8000
```

---

## Endpoints

### POST /predict

Classify a single text input into a geopolitical event category. Returns the predicted class label, the model's confidence score, and the derived severity level.

#### Request

```json
{
  "text": "string"
}
```

#### Response

```json
{
  "prediction": "conflict | protest | normal",
  "confidence": 0.0,
  "severity": "LOW | MEDIUM | HIGH | CRITICAL",
  "explanation": ["reason 1", "reason 2"]
}
```

| Field | Type | Description |
|---|---|---|
| `prediction` | `string` | Predicted class: `"conflict"`, `"protest"`, or `"normal"` |
| `confidence` | `float` | Softmax probability of the predicted class, in range `[0.0, 1.0]` |
| `severity` | `string` | Rule-based severity level: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"` |
| `explanation` | `array` | List of reasoning strings explaining the prediction |

#### Examples

**Conflict with critical keyword:**

Request:
```json
{ "text": "Missile strike reported near the capital" }
```

Response:
```json
{
  "prediction": "conflict",
  "confidence": 0.9812,
  "severity": "CRITICAL",
  "explanation": [
    "Missile or projectile terminology detected",
    "Aerial strike language identified",
    "Border conflict context found"
  ]
}
```

**Conflict without critical keyword:**

Request:
```json
{ "text": "Armed clashes reported on the border" }
```

Response:
```json
{
  "prediction": "conflict",
  "confidence": 0.9103,
  "severity": "HIGH",
  "explanation": [
    "Geopolitical conflict indicators present"
  ]
}
```

**Protest:**

Request:
```json
{ "text": "Mass protests erupted in the capital" }
```

Response:
```json
{
  "prediction": "protest",
  "confidence": 0.9642,
  "severity": "MEDIUM",
  "explanation": [
    "Protest activity language identified"
  ]
}
```

**Normal:**

Request:
```json
{ "text": "Trade negotiations concluded in Geneva" }
```

Response:
```json
{
  "prediction": "normal",
  "confidence": 0.8834,
  "severity": "LOW",
  "explanation": [
    "Diplomatic agreement language found",
    "Economic context identified"
  ]
}
```

#### Errors

- `422 Unprocessable Entity`: Invalid or missing JSON body.

---

### GET /news-analysis

Fetch live news from RSS, classify each article, derive confidence and severity, group by geographic region, and return intelligence output with weighted TES, anomaly status, and trend.

#### Request

No request body. No query parameters.

#### Response

Returns a JSON object keyed by region name. Each region contains:

| Field | Type | Description |
|---|---|---|
| `TES` | `float` | Confidence- and severity-weighted Threat Escalation Score (range `[0.0, 1.5]`) |
| `risk_score` | `float` | Duplicate of TES for frontend metric mapping |
| `risk_level` | `string` | Categorical risk level (`"LOW"`, `"MODERATE"`, `"HIGH"`, `"CRITICAL"`) |
| `anomaly` | `boolean` | Whether the region exceeds the anomaly threshold |
| `trend` | `string` | Temporal trend: `"increasing"`, `"decreasing"`, or `"stable"` |
| `events` | `array` | List of classified news events |

Each event in the `events` array:

| Field | Type | Description |
|---|---|---|
| `title` | `string` | Article headline |
| `prediction` | `string` | Classification: `"conflict"`, `"protest"`, or `"normal"` |
| `confidence` | `float` | Softmax probability of the predicted class, in range `[0.0, 1.0]` |
| `severity` | `string` | Rule-based severity level: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"` |
| `explanation` | `array` | List of reasoning strings explaining the prediction |

#### TES Calculation

```
event_score = prediction_weight × confidence × severity_multiplier
TES = average(event_score) over all events in the region
```

| Prediction | Weight | Severity | Multiplier |
|---|---|---|---|
| conflict | 1.0 | CRITICAL | 1.5 |
| protest | 0.6 | HIGH | 1.2 |
| normal | 0.2 | MEDIUM | 1.0 |
| — | — | LOW | 0.8 |

#### Example Response

```json
{
  "Middle East": {
    "TES": 1.2164,
    "risk_score": 1.2164,
    "risk_level": "CRITICAL",
    "anomaly": true,
    "trend": "increasing",
    "events": [
      {
        "title": "Airstrikes reported in northern Syria",
        "prediction": "conflict",
        "confidence": 0.9812,
        "severity": "CRITICAL",
        "explanation": ["Aerial strike language identified"]
      },
      {
        "title": "Armed clashes continue near the border",
        "prediction": "conflict",
        "confidence": 0.9103,
        "severity": "HIGH",
        "explanation": ["Border conflict context found"]
      },
      {
        "title": "Iran nuclear talks resume in Vienna",
        "prediction": "normal",
        "confidence": 0.7341,
        "severity": "LOW",
        "explanation": ["Diplomatic engagement context detected"]
      }
    ]
  },
  "South Asia": {
    "TES": 0.5285,
    "risk_score": 0.5285,
    "risk_level": "MODERATE",
    "anomaly": false,
    "trend": "stable",
    "events": [
      {
        "title": "Protests grow outside parliament in Islamabad",
        "prediction": "protest",
        "confidence": 0.8807,
        "severity": "MEDIUM",
        "explanation": ["Protest activity language identified", "Political process language identified"]
      },
      {
        "title": "India-Pakistan border tensions ease",
        "prediction": "normal",
        "confidence": 0.8107,
        "severity": "LOW",
        "explanation": ["Border conflict context found"]
      }
    ]
  }
}
```

---

## Risk Level Reference

The backend computes the categorical `risk_level` from the numeric TES value using these thresholds:

| TES Range | Risk Level | Frontend Color |
|---|---|---|
| >= 0.91 | `"CRITICAL"` | Red |
| >= 0.61 | `"HIGH"` | Orange |
| >= 0.31 | `"MODERATE"` | Yellow |
| < 0.31 | `"LOW"` | Green |

---

## Severity Level Reference

| Severity | Trigger Condition | Display Color |
|---|---|---|
| `CRITICAL` | `conflict` prediction + critical keyword in headline | Red |
| `HIGH` | `conflict` prediction + no critical keyword | Orange |
| `MEDIUM` | `protest` prediction | Yellow |
| `LOW` | `normal` prediction | Green |

Critical keywords: `missile`, `airstrike`, `explosion`, `terror`, `invasion`, `war`.

---

## Swagger UI

Interactive API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

## Future Endpoints

- `/batch-predict`: Classify multiple texts in a single request
- `/entities`: Named entity extraction from text
- `/timeline`: Historical analysis over time
