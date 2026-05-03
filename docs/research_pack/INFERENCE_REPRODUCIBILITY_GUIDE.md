# Inference Reproducibility Guide

This guide provides step-by-step instructions for running the bundled checkpoint
honestly and recording inference results responsibly. It targets reviewers,
researchers, and downstream users who want to verify the model's behaviour
without needing the training dataset.

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ezedeem223/waste-classification-transfer-learning.git
cd waste-classification-transfer-learning
```

### 2. Python Version

Python 3.10 or higher is required (see `pyproject.toml`).

```bash
python --version
# Expected: Python 3.10.x or higher
```

### 3. Install Runtime Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` pins:

```
numpy==1.26.0
pillow
tensorflow==2.17.0
```

GPU hardware is not required. CPU inference is supported.

### 4. Verify the Checkpoint

Before running inference, verify the checkpoint file integrity:

```bash
sha256sum models/vgg16_waste_classifier.keras
# Expected: 4d413b37716c5e23c8398ff533939c23359dd899b32aeec806b5e430df328ab0
```

On macOS:

```bash
shasum -a 256 models/vgg16_waste_classifier.keras
```

If the checksum does not match, do not use the file for inference; re-download
from the repository.

---

## Runtime Requirements

| Component | Requirement |
|---|---|
| Python | ≥ 3.10 |
| TensorFlow | 2.17.0 (pinned) |
| NumPy | 1.26.0 (pinned) |
| Pillow | Any recent version |
| GPU | Not required; CPU inference supported |
| Dataset | **Not required** for inference |
| Internet | Not required after cloning |

---

## Direct Prediction Command

```bash
python predict.py path/to/your/image.jpg
```

With explicit model path:

```bash
python predict.py path/to/your/image.jpg --model models/vgg16_waste_classifier.keras
```

---

## Model Path

Default: `models/vgg16_waste_classifier.keras`

If this file is absent, `predict.py` exits with a clear `FileNotFoundError`
message. Verify the file exists:

```bash
ls -lh models/vgg16_waste_classifier.keras
# Expected: ~99 MB file
```

---

## Input Image Expectations

| Property | Requirement |
|---|---|
| Format | Any format supported by Pillow (JPEG, PNG, WEBP, BMP, etc.) |
| Colour mode | RGB (Pillow converts automatically on load) |
| Minimum original resolution | No hard minimum; very low resolution may reduce reliability |
| Content | Single waste item or a clear dominant subject in the frame |
| Preprocessing | Handled automatically by `predict.py`; do not pre-resize manually |

The script automatically resizes the image to 150 × 150 pixels and rescales
pixel values to [0, 1]. Do not apply any preprocessing manually before passing
the image to `predict.py`.

---

## Output Interpretation

```
Model: models/vgg16_waste_classifier.keras
Predicted class: Organic (O)
Recyclable probability: 0.1821
Organic probability: 0.8179
```

| Output line | Meaning |
|---|---|
| `Model:` | Path to the checkpoint used |
| `Predicted class:` | `Organic (O)` or `Recyclable (R)` based on 0.5 threshold |
| `Recyclable probability:` | Raw sigmoid output ∈ [0, 1] |
| `Organic probability:` | `1 − recyclable_probability` |

**Important:** The probabilities are not calibrated. A `recyclable_probability`
of 0.95 does not guarantee the item is recyclable. Values near 0.5 indicate
high model uncertainty and should be flagged for human review.

---

## Failure Modes

| Symptom | Likely Cause | Action |
|---|---|---|
| `FileNotFoundError: Image file not found` | Image path is incorrect | Check the path |
| `FileNotFoundError: No default model checkpoint was found` | `models/vgg16_waste_classifier.keras` is absent | Verify the file exists; re-clone if needed |
| `ImportError: No module named tensorflow` | TF not installed | Run `pip install -r requirements.txt` |
| Unexpected prediction for a clearly organic/recyclable image | Model behaviour on out-of-distribution images | Note the input and probability; do not over-interpret |
| Very slow inference | TF loading time on CPU for large model | Expected; first inference call loads the model |

---

## What Can Be Verified Without the Dataset

| Check | Method |
|---|---|
| Checkpoint file integrity | SHA256 sum verification |
| Checkpoint file presence | `ls models/` |
| Inference runs without errors | `python predict.py path/to/any/image.jpg` |
| Output format matches documentation | Compare output lines to expected format |
| Unit tests pass | `pytest` (tests mock model loading; no dataset needed) |
| Research pack files exist | `python tools/evidence/validate_research_pack.py` |
| Preprocessing contract | Read `predict.py::load_image` |
| Output semantics | Read `predict.py::predict_image` |

---

## What Cannot Be Verified Without the Dataset

| Check | Reason |
|---|---|
| Reproduction of preserved accuracy metrics (0.83, 0.79, etc.) | Dataset required for evaluation |
| Reproduction of preserved precision/recall values | Dataset required |
| Calibration analysis | Dataset and calibration set required |
| Training curve regeneration | Dataset and notebook dependencies required |
| Confusion matrix (not present) | Dataset required; not produced in original notebook |
| Validation accuracy (0.8854) | Dataset required |

---

## How to Record Inference Runs Responsibly

When documenting inference results (e.g. in a research report or supplementary
material):

1. **Record the checkpoint checksum** used for the run:
   `4d413b37716c5e23c8398ff533939c23359dd899b32aeec806b5e430df328ab0`
2. **Record the TensorFlow version**: `tensorflow==2.17.0`
3. **Record the Python version** used.
4. **State the image source** (e.g. "publicly available image downloaded from X"
   or "personal photograph of [item description]").
5. **Do not claim** that a single inference result represents generalised model
   accuracy.
6. **Do not present** a high-confidence prediction as proof of calibrated
   probability.
7. **State clearly** that the model was run with `predict.py` using the
   bundled checkpoint.

Example responsible reporting statement:

> Inference was run using `predict.py` with the bundled checkpoint
> (`models/vgg16_waste_classifier.keras`, SHA256:
> `4d413b37716c5e23c8398ff533939c23359dd899b32aeec806b5e430df328ab0`)
> under TensorFlow 2.17.0 and Python 3.10. Individual inference results
> are qualitative illustrations of model behaviour and do not reproduce
> the preserved evaluation metrics, which were computed on the original
> held-out test set.

---

## Recommended Future Sample Gallery Requirements

A future sample gallery (without using unverified images) should meet the
following criteria before being committed:

1. **Clear provenance**: Each image must have a documented source and licence
   that permits redistribution in the repository.
2. **No fabricated examples**: Do not use AI-generated images presented as
   real waste items without disclosure.
3. **Representative diversity**: Include examples from both O and R classes,
   with varying backgrounds, lighting, and occlusion levels.
4. **Borderline cases**: Include examples with `recyclable_probability` near
   0.5 to illustrate model uncertainty.
5. **Named with prediction metadata**: Image filenames or a companion manifest
   should include the predicted class and probability for the documented run.
6. **Human-reviewed**: Each sample image in the gallery should be confirmed
   by a human reviewer to belong to the stated class.

No sample gallery is included in this repository at this time.
