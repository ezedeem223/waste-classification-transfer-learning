# Failure Mode Matrix

This matrix documents known and anticipated failure modes of the VGG16 binary
waste classifier. All entries are based on model design, task scope, and
preserved evaluation artifacts. No adversarial or stress-test evaluation was
performed in this documentation pass.

---

## Failure Mode Table

| # | Failure Mode | Affected Component | Why It Matters | Reviewer Risk | Detection / Mitigation | Safe Wording |
|---|---|---|---|---|---|---|
| 1 | Mixed waste in one image | Classifier output | Model produces one label per image; mixed-content frames will be labelled with whichever class features dominate | High — misclassification rate unknown on mixed frames | Flag images as multi-item via pre-screening; use human review for mixed frames | "single-label classifier; mixed-content images are outside the single-item assumption" |
| 2 | Dirty or occluded object | Feature extraction | Occlusion, soil, or debris covers discriminative visual features; model may rely on background or partial features | Medium-High | Reject images below a confidence threshold; request cleaner image capture | "occluded or dirty items may reduce classification reliability" |
| 3 | Ambiguous compostable packaging | Class boundary | Compostable packaging may visually resemble recyclable plastic; its correct class (O or R) may itself be ambiguous | High — label ambiguity cannot be resolved by the model | Human review required for ambiguous packaging types | "compostable items near the O/R boundary require human review" |
| 4 | Recyclable object with food residue | Class boundary | Residue introduces organic visual features onto a recyclable item; the correct practical label may differ from the visual label | High — contamination risk if classified as recyclable | Downstream inspection step; threshold adjustment toward Organic | "food-contaminated recyclables may be misclassified without downstream inspection" |
| 5 | Organic object in plastic container | Class boundary | Transparent container may cause model to respond to plastic features and predict Recyclable | Medium-High | Human review; protocol for containerised organics | "organic material in plastic containers may trigger recyclable predictions" |
| 6 | Unusual lighting | Feature extraction | Harsh shadows, overexposure, or artificial narrow-spectrum lighting distorts colour and texture features the model may rely on | Medium | Standardise capture conditions; augment training with lighting variation | "non-standard lighting conditions may reduce classification reliability" |
| 7 | Low resolution or blur | Preprocessing and features | Resizing a very low-resolution image to 150 × 150 introduces upscaling artefacts; blur removes fine texture detail | Medium | Reject images below a minimum original resolution; flag for human review | "blurry or very low-resolution images may produce unreliable outputs" |
| 8 | Background clutter | Feature extraction | Complex or visually similar backgrounds (e.g. natural debris, green leaves near organic items) may activate irrelevant features | Medium | Controlled capture environment; background subtraction pre-processing | "background clutter may interfere with classification; controlled capture is recommended" |
| 9 | Multiple objects in frame | Classifier output | Multiple distinct items in one image produce a single aggregated prediction that does not correspond to any individual item | High | Single-item image capture protocol; multi-label architecture if needed | "multiple objects in one frame produce a single ambiguous label" |
| 10 | Object outside O/R label space | Class boundary | Items that are neither clearly organic nor clearly recyclable (e-waste, hazardous material, non-recyclable plastics) are forced into one of two labels | High — silent misclassification with no rejection option | Out-of-distribution detection layer; human review for unknown categories | "items outside the O/R label space will be silently misclassified; an out-of-distribution detector is needed" |
| 11 | Dataset domain shift | Generalisation | Training images are from a curated dataset; real facility images may differ substantially in appearance | High — performance degradation magnitude is unknown | Domain adaptation study; target-domain validation set collection | "performance on images from domains different from the training set is not characterised" |
| 12 | Confidence misinterpretation | Output interpretation | Users may treat a high recyclable probability (e.g. 0.95) as a guarantee of correct classification; probabilities are not calibrated | High — misuse of model outputs | Clear documentation of probability semantics; calibration analysis before deployment | "model probabilities are not calibrated and must not be treated as guaranteed confidence scores" |
| 13 | Adversarial or misleading images | Robustness | Deliberately constructed inputs (adversarial perturbations) or misleading presentations can cause confident misclassification | Low in research context; relevant in any automated pipeline | Adversarial robustness evaluation; input validation | "no adversarial robustness evaluation has been performed" |
| 14 | Class imbalance effects | Evaluation interpretation | The evaluation test set has exactly 50 images per class (balanced); real-world waste streams may be heavily imbalanced, affecting practical precision/recall | Medium | Report precision/recall separately; evaluate on representative distribution | "preserved metrics are from a balanced 50/50 test set; real-world class distributions may differ" |
| 15 | Model file corruption or version mismatch | Inference pipeline | A corrupted or partially downloaded checkpoint produces errors or silently wrong predictions; loading with an incompatible TF version may fail | Low-Medium | Verify SHA256 checksum before use; pin TF to 2.17.0 | "verify the checkpoint SHA256 before use; see MODEL_RELEASE_CARD.md" |

---

## General Mitigation Principles

1. **Human review** is required for any borderline or high-stakes classification.
2. **Confidence thresholding** — consider rejecting predictions where
   `recyclable_probability` is between 0.4 and 0.6 and routing to human review.
3. **Image quality checks** — reject images below minimum resolution or
   flagged as multi-item before classification.
4. **Domain validation** — before using the model in a new image domain,
   collect and evaluate on a representative sample from that domain.
5. **Out-of-distribution detection** — add a rejection class or anomaly score
   for items not matching either O or R visual features.

---

## What This Matrix Is Not

- This matrix is not an exhaustive adversarial robustness study.
- Failure rates for each mode are not quantified; the dataset is not bundled
  and no stress-test evaluation was performed.
- This matrix should be updated with empirical findings when domain-specific
  evaluation data becomes available.
