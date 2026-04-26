# API Documentation

## Base URL

http://127.0.0.1:8000

---

## Endpoint: /predict

### Method

POST

---

## Request Format

```json
{
  "text": "string"
}
```

---

## Response Format

```json
{
  "prediction": "conflict | protest | normal"
}
```

---

## Example

### Request

```json
{
  "text": "Mass protests erupted in the capital"
}
```

### Response

```json
{
  "prediction": "protest"
}
```

---

## Error Handling

- Invalid JSON → 422 error
- Empty input → validation failure

---

## Future Endpoints

- /risk-score
- /batch-predict
- /entities
- /timeline
