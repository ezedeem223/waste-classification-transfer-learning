# Waste Model Release Evidence Pack

This directory contains institution-neutral research and model-release documentation
for the `waste-classification-transfer-learning` repository.

## Contents

| File | Purpose |
|---|---|
| [ACADEMIC_RESEARCH_BRIEF.md](ACADEMIC_RESEARCH_BRIEF.md) | Problem definition, approach, provenance caveats, future directions |
| [MODEL_CARD.md](MODEL_CARD.md) | Model family, inputs/outputs, intended use, limitations |
| [MODEL_RELEASE_CARD.md](MODEL_RELEASE_CARD.md) | Checkpoint governance, SHA256, release boundaries |
| [CHECKPOINT_AND_INFERENCE_CARD.md](CHECKPOINT_AND_INFERENCE_CARD.md) | CLI inference contract, preprocessing, output semantics |
| [METRIC_PROVENANCE_MATRIX.md](METRIC_PROVENANCE_MATRIX.md) | Per-metric source tracing and evidence confidence |
| [DATASET_AND_TASK_CARD.md](DATASET_AND_TASK_CARD.md) | Task scope, label space, dataset provenance and layout |
| [SUSTAINABILITY_USE_CASE_BOUNDARY.md](SUSTAINABILITY_USE_CASE_BOUNDARY.md) | Safe and unsafe sustainability claims |
| [FAILURE_MODE_MATRIX.md](FAILURE_MODE_MATRIX.md) | Known failure modes, risks, and mitigations |
| [CALIBRATION_AND_THRESHOLDING_PROTOCOL.md](CALIBRATION_AND_THRESHOLDING_PROTOCOL.md) | Probability calibration protocol and thresholding guidance |
| [INTERPRETABILITY_PROTOCOL.md](INTERPRETABILITY_PROTOCOL.md) | Visual explanation protocol and current artifact inventory |
| [INFERENCE_REPRODUCIBILITY_GUIDE.md](INFERENCE_REPRODUCIBILITY_GUIDE.md) | Step-by-step guide for running the bundled checkpoint honestly |
| [REPRODUCIBILITY_CHECKLIST.md](REPRODUCIBILITY_CHECKLIST.md) | Checklist for inference, training, and evaluation reproduction |

## Validation

```bash
python tools/evidence/validate_research_pack.py
```

## Scope

All documents in this directory are:

- Institution-neutral
- Based only on verified repository artifacts
- Careful not to overstate evaluation confidence
- Explicit about what requires the dataset versus only the checkpoint
- Free of fabricated metrics, confusion matrices, Grad-CAM outputs, or calibration plots

## Responsible-Use Boundaries

This evidence pack documents a **research prototype** for binary waste image
classification. It does not constitute operational recycling deployment guidance,
industry-level validation, or environmental impact measurement.
