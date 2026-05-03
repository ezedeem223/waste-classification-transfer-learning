# Model Card — VGG16 Waste Classifier

## Model Overview

| Field | Value |
|---|---|
| Model family | VGG16 transfer learning |
| Backbone | VGG16, pre-trained on ImageNet (`include_top=False`) |
| Classification head | Custom dense + dropout layers for binary output |
| Input size | 150 × 150 × 3 (RGB) |
| Preprocessing | Pixel values ÷ 255 → [0, 1] |
| Output | Single scalar `recyclable_probability` ∈ [0, 1] |
| Classes | `O` — Organic, `R` — Recyclable |
| Decision threshold | 0.5 (default in `predict.py`) |
| Fine-tuning | VGG16 layers from `block5_conv3` onward unfrozen |
| Framework | TensorFlow / Keras (recorded TF version: 2.17.0) |
| Checkpoint file | `models/vgg16_waste_classifier.keras` |

## Output Semantics

`predict.py` returns:

```
recyclable_probability  — model output (scalar sigmoid)
organic_probability     — 1 − recyclable_probability
predicted_class         — "Organic (O)" if recyclable_probability < 0.5
                          "Recyclable (R)" if recyclable_probability ≥ 0.5
```

The output probabilities are **not verified to be calibrated**. They should not
be interpreted as well-calibrated confidence scores without a separate
calibration analysis.

## Intended Research Use

- Baseline exploration of transfer learning for binary waste image classification
- Reproducibility and provenance reference for the documented training workflow
- Starting point for comparative studies or architecture ablations
- Research prototype for sustainability-oriented computer vision

## Out-of-Scope Uses

This model is **not** suitable, without further validation, for:

- Sorting operations at recycling or waste-processing facilities
- Industrial waste management automation
- Real-time high-throughput classification pipelines
- Material composition analysis
- Contamination detection
- Multi-class waste taxonomy beyond O/R
- Any deployment context where classification errors carry safety or
  regulatory consequences

## Dataset Status

- The training dataset is **not bundled** with this repository.
- The dataset used during training followed the layout described in `data/README.md`
  and `README.md`: an `o-vs-r-split/` directory with `train/` and `test/`
  subdirectories, each containing `O/` and `R/` image folders.
- Generator counts from the preserved notebook: 800 training images,
  200 validation images, 200 test images.
- Evaluation test set: 100 held-out images (50 organic, 50 recyclable).

## Checkpoint Status

- The bundled checkpoint **is present** at `models/vgg16_waste_classifier.keras`.
- Inference can be run without the dataset using `predict.py`.

## Preserved Evaluation Metrics

All metrics below are **preserved historical evaluation artifacts** from stored
notebook outputs. They were not newly reproduced in this documentation pass.

### Fine-Tuned Model (bundled checkpoint)

| Metric | Value | Source |
|---|---|---|
| Test accuracy | 0.83 | `outputs/fine_tuned_classification_report.txt` |
| Organic (O) precision | 0.80 | `outputs/fine_tuned_classification_report.txt` |
| Organic (O) recall | 0.88 | `outputs/fine_tuned_classification_report.txt` |
| Organic (O) F1-score | 0.84 | `outputs/fine_tuned_classification_report.txt` |
| Recyclable (R) precision | 0.87 | `outputs/fine_tuned_classification_report.txt` |
| Recyclable (R) recall | 0.78 | `outputs/fine_tuned_classification_report.txt` |
| Recyclable (R) F1-score | 0.82 | `outputs/fine_tuned_classification_report.txt` |
| Best validation accuracy | 0.8854 | `README.md` (notebook output) |
| Best validation loss | 0.2709 | `README.md` (notebook output) |
| Test set size | 100 (50 O + 50 R) | Support column in report |

### Extract-Features Model (reference)

| Metric | Value | Source |
|---|---|---|
| Test accuracy | 0.79 | `outputs/extract_features_classification_report.txt` |
| Organic (O) precision | 0.76 | `outputs/extract_features_classification_report.txt` |
| Organic (O) recall | 0.84 | `outputs/extract_features_classification_report.txt` |
| Recyclable (R) precision | 0.82 | `outputs/extract_features_classification_report.txt` |
| Recyclable (R) recall | 0.74 | `outputs/extract_features_classification_report.txt` |
| Best validation accuracy | 0.8802 | `README.md` (notebook output) |
| Best validation loss | 0.3567 | `README.md` (notebook output) |

**No confusion matrix artifact is present in this repository.**

## Known Technical Limitations

- Small training corpus (800 images); generalisation to unseen distributions
  is not guaranteed.
- Binary label space does not cover the full waste taxonomy.
- Default threshold (0.5) is not optimised for any application cost function.
- Domain shift from training distribution to real facility images is not
  characterised.
- No adversarial robustness evaluation has been performed.
- Model architecture inspection (input/output shape summary) was not performed
  via TensorFlow in this documentation pass; architecture is inferred from
  `predict.py` and `README.md`.

## Ethical and Safety Limitations

- Misclassification of recyclable items as organic (or vice versa) can cause
  contamination of recycling streams or loss of recoverable material.
- This model must not be used as the sole decision-maker in any waste
  management context. **Human review and downstream verification are required.**
- The model has not been evaluated for bias across different geographic
  contexts, cultural item presentations, or lighting conditions.
- Probability outputs are not calibrated and may overstate or understate
  confidence.

## Human-Review Requirement

Any downstream use of this model's outputs in a sorting or triage context
**must** include human review. The model is a research prototype and its
preserved evaluation metrics do not establish operational readiness.

## Waste-Stream Contamination Caveats

- A recyclable item contaminated with food residue may present visual features
  of an organic item and be misclassified.
- An organic item presented in clear plastic packaging may be misclassified as
  recyclable.
- Mixed-content images (multiple items of different classes in one frame)
  are outside the single-item classification assumption of this model.
- The model produces a single label per image and cannot indicate uncertainty
  about mixed or ambiguous content.
