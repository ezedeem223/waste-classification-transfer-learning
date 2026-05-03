# Reproducibility Checklist

Use this checklist to track what can and cannot be reproduced with the
resources currently available in this repository.

---

## 1. Installation

- [ ] Python ≥ 3.10 is available
- [ ] `pip install -r requirements.txt` completes without errors
  - numpy==1.26.0
  - pillow
  - tensorflow==2.17.0
- [ ] (Optional, for tests and linting) `pip install -r requirements-dev.txt`
- [ ] (Optional, for notebook) `pip install -r requirements-notebook.txt`

---

## 2. Inference with Bundled Checkpoint

**Can be verified without the dataset.**

- [ ] `models/vgg16_waste_classifier.keras` exists
- [ ] SHA256 of checkpoint matches:
  `4d413b37716c5e23c8398ff533939c23359dd899b32aeec806b5e430df328ab0`
- [ ] `python predict.py path/to/image.jpg` runs without error
- [ ] Output format matches:
  ```
  Model: models/vgg16_waste_classifier.keras
  Predicted class: <Organic (O) or Recyclable (R)>
  Recyclable probability: <float>
  Organic probability: <float>
  ```
- [ ] `predict.py --help` shows expected argument descriptions
- [ ] `python predict.py missing.jpg` exits with `FileNotFoundError` message
- [ ] `python predict.py image.jpg --model missing.keras` exits with `FileNotFoundError` message

---

## 3. Unit Tests

**Can be verified without the dataset.**

- [ ] `pytest` completes with all tests passing
- [ ] Tests verify:
  - Missing model path raises `FileNotFoundError`
  - Missing image path raises `FileNotFoundError`
  - `load_image` returns batch of shape `(1, 150, 150, 3)` with dtype `float32`
  - `load_image` values are in [0.0, 1.0]
  - `predict_image` with mocked model returns correct class label and probability
- [ ] Research pack existence tests pass (`tests/test_research_pack_exists.py`)
- [ ] Metric provenance tests pass (`tests/test_metric_provenance.py`)

---

## 4. Research Pack Validation

**Can be verified without the dataset.**

- [ ] `python tools/evidence/validate_research_pack.py` passes all checks
- [ ] No forbidden phrases found in `docs/research_pack/`
- [ ] All required research pack files are present

---

## 5. Dataset Setup

**Required for training and evaluation reproduction.**

- [ ] Dataset placed at `data/o-vs-r-split/`
- [ ] Structure verified:
  ```
  data/o-vs-r-split/
  ├── train/
  │   ├── O/   (organic training images)
  │   └── R/   (recyclable training images)
  └── test/
      ├── O/   (organic test images)
      └── R/   (recyclable test images)
  ```
- [ ] Approximately 800 training images present (per preserved notebook metadata)
- [ ] Test set contains 50 O + 50 R images (per preserved notebook metadata)

---

## 6. Notebook and Training Rerun

**Requires dataset. Cannot run without `data/o-vs-r-split/` present.**

- [ ] Notebook dependencies installed: `pip install -r requirements-notebook.txt`
- [ ] Jupyter environment available
- [ ] `notebooks/main.ipynb` opened and kernel set to Python 3.10 environment
- [ ] Optional dataset download cell run (if dataset is absent)
- [ ] All notebook cells run in order without errors
- [ ] Training curves regenerated in `outputs/`
- [ ] Evaluation reports regenerated in `outputs/`
- [ ] New checkpoint saved (will differ from bundled checkpoint if random seed differs)

**Note:** Regenerated metrics may differ from preserved values due to:
- Random seed variation
- TensorFlow version differences
- Hardware differences (CPU vs. GPU numerics)
- Data ordering differences

---

## 7. Required Local Assets

| Asset | Required For | Bundled? |
|---|---|---|
| `models/vgg16_waste_classifier.keras` | Inference | **Yes** |
| `data/o-vs-r-split/` | Training / evaluation | **No** |
| `outputs/*.txt` | Metric reference | **Yes** |
| `outputs/*.png` | Visual reference | **Yes** |
| `notebooks/main.ipynb` | Notebook rerun | **Yes** |

---

## 8. What Can Be Verified Without the Dataset

| Item | Status |
|---|---|
| Checkpoint file presence and integrity | Verifiable (SHA256) |
| Inference runs correctly | Verifiable with any image |
| Output format is correct | Verifiable |
| Unit tests pass | Verifiable |
| Linting passes (`ruff check .`) | Verifiable |
| Research pack files are present | Verifiable |
| Forbidden phrases absent from docs | Verifiable |
| Validation tool passes | Verifiable |

---

## 9. What Cannot Be Verified Without the Dataset

| Item | Reason |
|---|---|
| Preserved test accuracy (0.83) | Evaluation requires dataset |
| Preserved precision/recall/F1 values | Evaluation requires dataset |
| Best validation accuracy (0.8854) | Training requires dataset |
| Best validation loss (0.2709) | Training requires dataset |
| Calibration analysis | Calibration set required |
| New training curve generation | Training requires dataset |
| Confusion matrix (not present; not claimed) | Evaluation requires dataset |
| Notebook rerun | Dataset + notebook deps required |

---

## 10. Expected Outputs After Full Rerun (With Dataset)

| Output | Expected Location |
|---|---|
| Training loss/accuracy curves | `outputs/extract_features_loss_curve.png`, etc. |
| Classification reports | `outputs/evaluation_reports.txt`, `outputs/*_classification_report.txt` |
| Prediction examples | `outputs/*_prediction_example_*.png` |
| New checkpoint | `models/` (location configurable in notebook) |

**Note:** Regenerated checkpoints will have a different SHA256 from the
bundled checkpoint. The bundled checkpoint is the canonical release artifact.

---

## 11. Limitations

- The bundled checkpoint cannot be reconstructed exactly from the notebook
  rerun unless the original random seed, dataset order, and TF environment
  are precisely reproduced.
- The dataset is not included; its provenance and licence must be verified
  from the upstream source.
- No confusion matrix artifact was produced in the original notebook run;
  none is expected from a rerun unless explicitly added.
- Calibration analysis, Grad-CAM outputs, and saliency maps are not part of
  the current notebook and require additional implementation.
- Performance on images from domains different from the training set is not
  characterised.
