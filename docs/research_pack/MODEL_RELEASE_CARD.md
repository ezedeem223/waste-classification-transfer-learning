# Model Release Card — VGG16 Waste Classifier Checkpoint

## Checkpoint Identity

| Field | Value |
|---|---|
| Checkpoint path | `models/vgg16_waste_classifier.keras` |
| File present | Yes (verified) |
| File size | 104,061,021 bytes (≈ 99.24 MB) |
| SHA256 checksum | `4d413b37716c5e23c8398ff533939c23359dd899b32aeec806b5e430df328ab0` |
| Format | Keras native format (`.keras`) |
| TF version at training | 2.17.0 (recorded in notebook environment) |

To verify the checksum locally:

```bash
sha256sum models/vgg16_waste_classifier.keras
# or on macOS:
shasum -a 256 models/vgg16_waste_classifier.keras
```

Expected: `4d413b37716c5e23c8398ff533939c23359dd899b32aeec806b5e430df328ab0`

## Expected Input Shape

- Shape: `(1, 150, 150, 3)` — batch of one 150 × 150 RGB image
- Dtype: `float32`
- Value range: [0.0, 1.0] — pixel values divided by 255

This is verified from `predict.py` (`IMAGE_SIZE = (150, 150)` and the
`/ 255.0` rescaling in `load_image`).

## Expected Preprocessing Contract

```python
image = tf.keras.utils.load_img(image_path, target_size=(150, 150))
array = tf.keras.utils.img_to_array(image).astype("float32") / 255.0
batch = np.expand_dims(array, axis=0)  # shape: (1, 150, 150, 3)
```

Deviation from this preprocessing contract will produce unreliable outputs.

## Expected Output

- Shape: `(1, 1)` — single sigmoid scalar per image
- Dtype: `float32`
- Semantics: `recyclable_probability` ∈ [0, 1]
- `organic_probability = 1 − recyclable_probability`
- Default label assignment:
  - `recyclable_probability < 0.5` → `"Organic (O)"`
  - `recyclable_probability ≥ 0.5` → `"Recyclable (R)"`

Output shape and semantics are inferred from `predict.py`. Direct TensorFlow
model summary inspection was not performed in this documentation pass.

## Output Labels

| Index | Label | Condition |
|---|---|---|
| 0 | Organic (O) | `recyclable_probability < 0.5` |
| 1 | Recyclable (R) | `recyclable_probability ≥ 0.5` |

## Runtime Dependency Notes

Install only:

```bash
pip install -r requirements.txt
```

`requirements.txt` pins:

```
numpy==1.26.0
pillow
tensorflow==2.17.0
```

Training and notebook dependencies (`requirements-notebook.txt`) are **not**
required for inference. Development/lint dependencies (`requirements-dev.txt`)
are not required for inference.

## How to Run Inference

```bash
# Default checkpoint (models/vgg16_waste_classifier.keras)
python predict.py path/to/image.jpg

# Explicit checkpoint path
python predict.py path/to/image.jpg --model models/vgg16_waste_classifier.keras
```

Example output:

```
Model: models/vgg16_waste_classifier.keras
Predicted class: Organic (O)
Recyclable probability: 0.1821
Organic probability: 0.8179
```

## What This Release Includes

- `models/vgg16_waste_classifier.keras` — fine-tuned binary classifier checkpoint
- `predict.py` — maintained direct inference script
- `outputs/` — preserved training curves, evaluation reports, and prediction
  example images (qualitative, from notebook outputs)
- `notebooks/main.ipynb` — preserved original training notebook
- `requirements.txt` — runtime dependency pins
- `tests/` — unit tests for `predict.py` logic
- `docs/research_pack/` — model-release documentation and evidence pack

## What This Release Does Not Include

- Training dataset (intentionally excluded; not bundled)
- Raw sample input images (not bundled; see Repository Notes in README.md)
- Confusion matrix artifact (not present; not claimed)
- Calibrated probability outputs
- Grad-CAM or saliency visualisations
- Validation set or test set images
- Multi-class extension of the model
- Adversarial robustness evaluation
- Production deployment artefacts

## Known Limitations

- No guarantee of performance beyond the preserved test set conditions.
- SHA256 checksum verifies file integrity, not model correctness or
  representational quality.
- Outputs are not calibrated probabilities.
- The checkpoint was saved with TensorFlow 2.17.0; loading with substantially
  different TensorFlow versions may produce warnings or require compatibility
  handling.
- The checkpoint size (~99 MB) is relatively large for a standard Git
  repository; Git LFS may be advisable for forks or CI environments with
  size constraints.

## Responsible-Use Boundaries

- This checkpoint is released as a **research prototype** and a
  **model-release artifact** for academic and reproducibility purposes.
- It is **not** released as an operational waste-sorting system component.
- It is **not** validated against real facility waste streams.
- It is **not** cleared for any use context where classification errors carry
  safety, regulatory, or environmental accountability.
- Any downstream application must include human review and independent
  domain validation before operational use.

## Reproducibility Caveats

- The preserved evaluation metrics were computed in the original notebook
  training session. Fresh reproduction of those exact metrics requires the
  original dataset, the recorded TF environment, and the steps documented in
  `notebooks/main.ipynb`.
- Inference reproducibility (consistent output for a fixed input) can be
  verified without the dataset using the bundled checkpoint and `predict.py`.
