# Calibration and Thresholding Protocol

## Important Statement

**No calibration results are generated in this pass.**

No calibration plots, reliability curves, Brier scores, or calibrated
probability outputs were produced in this documentation pass. The dataset
required for calibration is not bundled in this repository.

---

## Why Accuracy Alone Is Insufficient

A classifier with 0.83 test accuracy can still produce poorly calibrated
probabilities. A model is **calibrated** if, among all predictions where it
assigns probability *p* to the positive class, approximately a fraction *p*
of those predictions are correct. Without calibration analysis:

- A `recyclable_probability` of 0.9 may not correspond to 90% empirical
  accuracy at that score level.
- High-confidence predictions may be systematically over- or under-confident.
- Threshold selection based on raw probabilities may not achieve the intended
  precision/recall trade-off.

This is particularly important for waste classification because the cost of
false positives (false recyclable) and false negatives (false organic) differ
materially in most application contexts.

---

## Probability Calibration

### What It Is

Calibration analysis measures the agreement between predicted probabilities
and observed frequencies. A perfectly calibrated binary classifier satisfies:

```
P(Y = 1 | f(x) = p) = p  for all p ∈ [0, 1]
```

where `f(x)` is the model's output probability.

### Why It Matters Here

The VGG16 classifier uses a sigmoid output layer. Sigmoid outputs are not
guaranteed to be calibrated. Transfer learning and fine-tuning with limited
data can produce overconfident or underconfident outputs.

### Calibration Methods (for future implementation)

| Method | Description | When to Use |
|---|---|---|
| Platt scaling | Logistic regression on model outputs | Widely applicable; simple |
| Temperature scaling | Divide logits by a scalar T before sigmoid | Common for neural networks; single parameter |
| Isotonic regression | Non-parametric monotone calibration | More data required |
| Beta calibration | Beta distribution fit to outputs | Binary classifiers |

Calibration requires a held-out **calibration set** (distinct from the test
set). It cannot be performed without the dataset.

---

## Reliability Curves

A reliability diagram (calibration curve) plots:
- X axis: Mean predicted probability in each probability bin
- Y axis: Fraction of positive (Recyclable) instances in each bin
- Ideal: Points fall on the diagonal (y = x)

No reliability diagram is present in this repository. Generating one
requires the dataset and a calibration set.

**Required artifacts (not present):**
- `outputs/calibration_reliability_curve.png`
- Calibration set predictions and labels

---

## Brier Score

The Brier score measures mean squared error between predicted probabilities
and true binary labels:

```
BS = (1/N) * sum((p_i - y_i)^2)
```

Lower is better (0 = perfect, 0.25 = uninformative baseline for balanced
binary classification).

No Brier score is computed in this pass. It requires the dataset and model
predictions over a held-out set.

---

## Threshold Selection

### Current Default

`predict.py` applies a fixed threshold of **0.5**:

```python
predicted_index = 0 if recyclable_probability < 0.5 else 1
```

This threshold is not optimised for any application cost function.

### Threshold Trade-Offs

| Threshold Direction | Effect on Recyclable Predictions | Effect on Organic Predictions |
|---|---|---|
| Increase threshold (e.g. 0.6) | Fewer items classified as Recyclable; higher Recyclable precision | More items classified as Organic; higher Organic recall |
| Decrease threshold (e.g. 0.4) | More items classified as Recyclable; higher Recyclable recall | Fewer items classified as Organic; higher Organic precision |

### Precision/Recall Trade-Offs Between O and R

From the preserved evaluation artifacts (fine-tuned model):

| Class | Precision | Recall |
|---|---|---|
| Organic (O) | 0.80 | 0.88 |
| Recyclable (R) | 0.87 | 0.78 |

The fine-tuned model has higher recall for Organic and higher precision for
Recyclable at the default 0.5 threshold. This means the model tends to
capture more organic items correctly (fewer false organics missed) while
being more conservative about declaring recyclable (fewer false recyclables).

Whether this trade-off is appropriate depends on the application cost
function — which has not been defined for this research prototype.

---

## Cost Sensitivity

### False Recyclable (Organic classified as Recyclable)

An organic item entering the recyclable stream causes contamination. Depending
on the facility and material, a single contaminated batch may render a larger
volume of recyclable material unprocessable. This error type may have
**asymmetrically high cost** in real sorting contexts.

Mitigation: Increase the classification threshold above 0.5 to reduce false
recyclable predictions at the cost of lower recyclable recall.

### False Organic (Recyclable classified as Organic)

A recyclable item routed to the organic stream is lost from the recycling
capture. This reduces the fraction of material recovered for recycling.
This error type has **lower immediate contamination risk** but accumulates
as a recovery efficiency loss.

Mitigation: Decrease the classification threshold to increase recyclable
recall at the cost of lower recyclable precision.

### Cost Function Definition

A formal cost function should specify:
- Cost of false recyclable (C_FR)
- Cost of false organic (C_FO)
- Optimal threshold: p* = C_FR / (C_FR + C_FO) applied to calibrated probabilities

No cost function has been defined for this project. No optimal threshold
has been computed.

---

## Required Future Artifacts

To complete a calibration and thresholding analysis, the following are needed:

| Artifact | Requires |
|---|---|
| Calibration set predictions | Dataset + model + predict.py |
| Reliability curve (PNG) | Calibration set predictions + matplotlib |
| Brier score | Calibration set predictions |
| Precision-recall curve | Test set predictions |
| ROC curve with AUC | Test set predictions |
| Optimal threshold analysis | Defined cost function + calibrated probabilities |
| Temperature scaling parameter | Calibration set + logit-level access |

---

## Safe Wording

| Safe | Unsafe |
|---|---|
| "model probabilities are not verified to be calibrated" | "the model is calibrated" |
| "threshold selection requires application-specific cost function definition" | "the 0.5 threshold is optimal" |
| "calibration analysis is required before probability-based decision making" | "confidence scores are reliable" |
| "false recyclable and false organic errors have different costs" | "the model minimises contamination" |

---

## Summary

The bundled checkpoint produces sigmoid probability outputs that are not
calibrated. The default threshold of 0.5 is not tuned for any application.
Calibration and threshold optimisation require the dataset and a defined
application cost function. No calibration results are generated in this pass.
