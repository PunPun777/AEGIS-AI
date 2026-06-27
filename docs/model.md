# Model Documentation

## Model Type

- Architecture: DistilBERT
- Task: Multi-class text classification
- Framework: Hugging Face Transformers + PyTorch

---

## Classes

| Label | Meaning  |
| ----- | -------- |
| 0     | Conflict |
| 1     | Normal   |
| 2     | Protest  |

---

## Training Dataset

- Base dataset: AG News
- Custom relabeling using keyword heuristics

---

## Labeling Logic

- Protest keywords → protest
- Conflict keywords → conflict
- Otherwise → normal

---

## Training Configuration

- Learning rate: 2e-5
- Epochs: 2–3
- Batch size: 16
- Loss: Cross-entropy

---

## Inference Pipeline

1. Input text
2. Tokenization (AutoTokenizer)
3. Model forward pass (no gradient)
4. Softmax over logits → probability distribution
5. Argmax → predicted class index
6. Confidence extraction → `probabilities[0][pred_index].item()`
7. Label mapping via `LABEL_MAP`
8. Severity assignment via `severity_service.get_severity(prediction, text)`

The inference function returns `prediction`, `confidence`, and `severity` in a single pass.

---

## Confidence Score

The confidence score is the softmax probability of the predicted class. It quantifies how strongly the model favors the selected class over the alternatives, normalized across all classes.

- **Range**: `[0.0, 1.0]`
- **Derivation**: `F.softmax(logits, dim=-1)[0][pred_index]`
- **Precision**: Rounded to 4 decimal places
- **Formatting**: Raw float returned by the API; percentage conversion is the responsibility of the frontend

A confidence of `0.96` means the model assigned 96% of its probability mass to the predicted class. A confidence below `0.70` signals low certainty and may indicate ambiguous input.

---

## Severity Classification

Severity is not produced by the model. It is assigned by `severity_service.py` using a rule-based approach applied after inference.

| Prediction | Base Severity | Escalation Condition | Escalated Severity |
|---|---|---|---|
| `normal` | `LOW` | N/A | N/A |
| `protest` | `MEDIUM` | N/A | N/A |
| `conflict` | `HIGH` | Critical keyword in text | `CRITICAL` |

Critical keywords: `missile`, `airstrike`, `explosion`, `terror`, `invasion`, `war`.

Severity is deterministic given the same prediction and text input. It does not use model probabilities.

---

## Evaluation Metrics

- Accuracy
- F1 Score
- Precision
- Recall

---

## Observations

- High accuracy (~97–99%)
- Strong keyword detection
- Limited semantic generalization
- Confidence scores skew high due to heuristic training labels; values should be interpreted relative to each other rather than as calibrated probabilities
- Severity is entirely rule-based; it reflects lexical escalation signals, not deeper semantic understanding

---

## Known Issues

- Misclassification of edge cases
- Over-reliance on keywords
- Limited contextual reasoning
- Confidence scores are not calibrated (temperature scaling not applied)
- Severity keyword list is fixed and does not adapt to emerging terminology

---

## Future Improvements

- Train on real geopolitical datasets
- Apply confidence calibration (temperature scaling, Platt scaling)
- Replace rule-based severity with a learned severity classifier
- Add contextual embeddings
- Use multi-label classification
- Incorporate sentiment + NER
