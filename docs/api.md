# API Documentation

## Base URL

```
http://127.0.0.1:8000
```

---

## Endpoints

### POST /predict

Classify a single text input into a geopolitical event category.

#### Request

```json
{
  "text": "string"
}
```

#### Response

```json
{
  "prediction": "conflict | protest | normal"
}
```

#### Example

**Request:**
```json
{
  "text": "Mass protests erupted in the capital"
}
```

**Response:**
```json
{
  "prediction": "protest"
}
```

#### Errors

- `422 Unprocessable Entity`: Invalid or missing JSON body.

---

### GET /news-analysis

Fetch live news from RSS, classify each article, group by geographic region, and return intelligence output with TES, anomaly status, and trend.

#### Request

No request body. No query parameters.

#### Response

Returns a JSON object keyed by region name. Each region contains:

| Field | Type | Description |
|---|---|---|
| `TES` | `float` | Threat Escalation Score (0.0 - 1.0) |
| `anomaly` | `boolean` | Whether the region exceeds the anomaly threshold |
| `trend` | `string` | Temporal trend: "increasing", "decreasing", or "stable" |
| `events` | `array` | List of classified news events |

Each event in the `events` array:

| Field | Type | Description |
|---|---|---|
| `title` | `string` | Article headline |
| `prediction` | `string` | Classification: "conflict", "protest", or "normal" |

#### Example Response

```json
{
  "Middle East": {
    "TES": 0.87,
    "anomaly": true,
    "trend": "increasing",
    "events": [
      {
        "title": "Airstrikes reported in northern Syria",
        "prediction": "conflict"
      },
      {
        "title": "Iran nuclear talks resume in Vienna",
        "prediction": "normal"
      }
    ]
  },
  "South Asia": {
    "TES": 0.40,
    "anomaly": false,
    "trend": "stable",
    "events": [
      {
        "title": "India-Pakistan border tensions ease",
        "prediction": "normal"
      }
    ]
  }
}
```

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
