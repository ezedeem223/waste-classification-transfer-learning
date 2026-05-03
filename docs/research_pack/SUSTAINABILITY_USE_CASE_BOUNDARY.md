# Sustainability Use-Case Boundary

## Purpose

This document defines the boundary between what sustainability-related claims
are reasonably supported by this research prototype and what claims are not
supported and must not be made.

---

## What Sustainability Claim Is Reasonable

The following claims are supported by the repository's documented scope and
preserved evaluation artifacts:

- This project **supports research exploration of AI-assisted waste image
  classification** at the binary O/R level.
- The documented baseline demonstrates that **VGG16 transfer learning can
  distinguish organic from recyclable waste images** at modest accuracy on a
  controlled dataset split.
- This work **contributes a reproducible transfer-learning baseline** to the
  academic literature on sustainability-oriented computer vision.
- The bundled checkpoint and preserved evaluation artifacts provide a
  **starting reference point** for future research into improved waste
  classification models.
- The approach **could be extended into sorting-support workflows after
  domain validation**, independent verification, and human-review integration.

---

## What Cannot Be Claimed

The following claims are **not supported** by this repository and must not be
made in any context that references this work:

| Unsupported Claim | Reason |
|---|---|
| Reduces recycling contamination | No contamination rate measurement was performed; model accuracy on a controlled test set does not translate to contamination reduction |
| Improves recycling efficiency in any facility | No facility-level deployment or measurement has occurred |
| Quantified environmental impact | No environmental impact measurement has been conducted |
| Validated industrial sorting system | No validation against industrial sorting systems has been performed |
| Operational waste sorting readiness | The model is a research prototype, not a validated operational component |
| Accuracy guarantees for sorting | Accuracy on a 100-image test set does not guarantee performance in deployment |
| Environmental benefit quantification | No lifecycle analysis or carbon footprint measurement is present |
| Real-world contamination reduction | Not operational; impact is not measured |

---

## Difference Between Image Classification and Actual Recycling Impact

Image classification accuracy on a controlled test set and real-world recycling
impact are separated by multiple steps, each of which introduces uncertainty:

1. **Domain shift** — images in the training/test set are curated photographs;
   images in a real facility may differ in lighting, angle, occlusion,
   resolution, and item presentation.
2. **Single-item assumption** — the model classifies one item per image. Real
   waste streams contain mixed, overlapping, or partially visible items.
3. **Classification to sorting** — a classification output must be connected
   to a physical sorting action. The reliability of that connection depends on
   system design, actuator precision, and rejection handling.
4. **Sorting accuracy to stream purity** — stream purity depends on the
   fraction of items classified correctly, the volume of edge cases, and
   downstream processing.
5. **Stream purity to environmental impact** — only some fraction of sorted
   recyclable material is ultimately recycled; contamination thresholds,
   market conditions, and facility processes determine actual recycling yield.

None of steps 2–5 have been studied or validated in this project.

---

## Contamination Risk

- A **false recyclable** prediction (organic item classified as recyclable)
  introduces organic contamination into a recycling stream. This can render
  batches of recyclable material unprocessable and increase facility costs.
- A **false organic** prediction (recyclable item classified as organic)
  causes loss of potentially recoverable material.
- The **relative cost** of these two error types depends on the application
  context and is not addressed by the default 0.5 threshold in `predict.py`.

---

## Operational Sorting Constraints

Operational waste sorting systems involve constraints not addressed by this
research prototype:

- Throughput requirements (items per minute)
- Real-time latency constraints
- Physical sensor integration (conveyor cameras, depth sensors)
- Robustness to occlusion, lighting variation, and debris
- Regulatory and liability requirements
- Auditing and traceability requirements

None of these are addressed in this repository.

---

## Domain Shift from Controlled Dataset to Facility Images

The training dataset is a curated split of labelled waste images. Facility
images may differ substantially in:

- Background complexity (conveyor belts, mixed debris)
- Lighting (artificial, variable, directional)
- Image resolution and motion blur
- Object presentation (crushed, wet, torn, partially buried)
- Camera angle and distance
- Geographic and cultural variation in waste presentation

Domain shift magnitude has not been characterised. Performance on facility
images may be materially lower than the preserved 0.83 test accuracy.

---

## Human Review and Downstream Verification Requirement

Any use of this model's outputs in a decision-making context **must** include:

- Human review of uncertain cases (probability near 0.5)
- Independent verification of classification quality on the target domain
- A defined process for handling misclassification consequences

The model must not be used as the sole decision-maker in any sorting or
triage context.

---

## How This Project Could Fit Into Future Sustainability Workflows

With appropriate further work, this prototype could serve as:

- A **baseline comparator** in a study that introduces improved architectures
  or multi-class waste taxonomies
- A **starting checkpoint** for domain adaptation experiments using facility
  images
- A **data collection tool** in a research context where human annotators
  review and correct model predictions to build a more representative dataset
- One **signal among several** in a human-assisted triage workflow where a
  human operator reviews model-flagged items

Each of these applications would require independent validation before
sustainability impact claims could be made.

---

## Evidence Required Before Environmental Impact Claims

Before any environmental impact claim could responsibly accompany work
derived from this project, the following evidence would be needed:

1. Domain validation on images from the target deployment environment
2. Prospective accuracy measurement on in-distribution operational images
3. Contamination rate measurement before and after system introduction
4. Statistical analysis connecting classification accuracy to stream purity
5. Lifecycle analysis or material flow analysis connecting stream purity to
   environmental outcomes
6. Independent audit of the sorting system and its operational parameters

None of this evidence is present in or implied by this repository.

---

## Not Operational

This project is **not operational**. It is a research prototype. Preserved
evaluation metrics document model performance on a controlled historical
dataset split and do not establish operational readiness or environmental
benefit.
