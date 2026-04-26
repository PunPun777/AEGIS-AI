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
2. Tokenization
3. Model forward pass
4. Argmax classification
5. Label mapping

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

---

## Known Issues

- Misclassification of edge cases
- Over-reliance on keywords
- Limited contextual reasoning

---

## Future Improvements

- Train on real geopolitical datasets
- Add contextual embeddings
- Use multi-label classification
- Incorporate sentiment + NER
