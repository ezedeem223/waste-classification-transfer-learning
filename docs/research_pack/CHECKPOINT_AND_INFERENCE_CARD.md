# Checkpoint and Inference Card

## Default Inference Command

```bash
python predict.py path/to/image.jpg
```

Optional explicit model path:

```bash
python predict.py path/to/image.jpg --model models/vgg16_waste_classifier.keras
```

## Expected CLI Input

| Argument | Required | Description |
|---|---|---|
| `image` | Yes | Path to image file (JPEG, PNG, or any format supported by Pillow) |
| `--model` | No | Path to a `.keras` checkpoint; defaults to `models/vgg16_waste_classifier.keras` |

## Default Model Path

`models/vgg16_waste_classifier.keras`

If this file is absent, `predict.py` raises `FileNotFoundError` with an
explicit message. The file is bundled in the repository.

## Image Preprocessing Contract

All of the following steps must be applied, in order, before passing an image
to the model. They are implemented in `predict.py::load_image`:

1. Load image from disk using `tf.keras.utils.load_img`
2. Resize to **150 × 150** pixels (RGB)
3. Convert to `float32` array via `tf.keras.utils.img_to_array`
4. Divide all pixel values by **255.0** → range [0.0, 1.0]
5. Add batch dimension → shape `(1, 150, 150, 3)`

Deviating from this contract (e.g. different resize, different scaling,
BGR channel order) will produce unreliable or meaningless outputs.

## Class Probability Semantics

| Output name | Meaning | Formula |
|---|---|---|
| `recyclable_probability` | Model sigmoid output | Raw model output ∈ [0, 1] |
| `organic_probability` | Complement | `1 − recyclable_probability` |

The model produces a single sigmoid scalar. It does not produce separate
logits for each class.

## Thresholding Assumption

The default decision boundary is **0.5**:

```
recyclable_probability < 0.5  →  Predicted: "Organic (O)"
recyclable_probability ≥ 0.5  →  Predicted: "Recyclable (R)"
```

This threshold is fixed in `predict.py` and is **not** tuned for any
application-specific cost function (e.g. minimising false recyclable rate).
See `CALIBRATION_AND_THRESHOLDING_PROTOCOL.md` for guidance on threshold
selection.

## Output Format

```
Model: models/vgg16_waste_classifier.keras
Predicted class: Organic (O)
Recyclable probability: 0.1821
Organic probability: 0.8179
```

All four lines are printed to standard output. `predict.py` exits with code 0
on success and raises `SystemExit` on `FileNotFoundError`.

## Error Modes

| Error | Cause | Output |
|---|---|---|
| `FileNotFoundError: Image file not found` | Image path does not exist | `SystemExit` with message |
| `FileNotFoundError: Model file not found` | Explicit `--model` path does not exist | `SystemExit` with message |
| `FileNotFoundError: No default model checkpoint was found` | `models/vgg16_waste_classifier.keras` absent and no `--model` given | `SystemExit` with message |
| Pillow decode error | Unsupported or corrupted image file | Unhandled exception from Pillow |
| TensorFlow import error | `tensorflow` not installed | `ImportError` at startup |

## Model File Availability

The checkpoint is **bundled** in the repository at
`models/vgg16_waste_classifier.keras`. Inference does not require internet
access or the training dataset.

## Dataset Independence for Inference

Inference with the bundled checkpoint requires:

- Python ≥ 3.10
- Dependencies from `requirements.txt` (`numpy==1.26.0`, `pillow`, `tensorflow==2.17.0`)
- The bundled checkpoint file
- An image file to classify

Inference does **not** require:

- The training dataset
- Notebook dependencies (`requirements-notebook.txt`)
- Any internet connection
- GPU hardware (CPU inference is supported)

## Limitations of Single-Image Inference

- One image produces one label. Mixed-content images (multiple items of
  different classes in a single frame) are outside the single-label
  classification assumption.
- The model processes each image independently. There is no temporal context,
  sequence modelling, or multi-view fusion.
- Unusual camera angles, extreme lighting, heavy occlusion, or image
  resolution substantially below 150 × 150 (after resizing introduces
  artefacts) may reduce reliability.
- Each inference call reloads the model from disk. Batch inference or
  warm-loaded model reuse is not implemented in `predict.py` but can be
  constructed from the public functions (`load_image`, `predict_image`).

## Safe Interpretation of Probabilities

- A `recyclable_probability` of 0.92 means the model assigns high confidence
  to the Recyclable class **given this input and its training distribution**.
  It does not mean there is a 92% probability the item is recyclable in a
  physical or legal sense.
- Probabilities near 0.5 indicate the model is uncertain and the input should
  receive additional human review.
- Probabilities are **not** calibrated. High or low probability values may
  not accurately reflect the true empirical frequency of correct predictions
  at that score level.
- Do not treat model output as a substitute for expert human review in any
  sorting or compliance context.

## Separation of Inference, Training, and Notebook Reproduction

| Capability | Requires dataset? | Requires notebook deps? | Requires GPU? |
|---|---|---|---|
| Single-image inference (`predict.py`) | No | No | No |
| Unit tests (`pytest`) | No | No | No |
| Training / evaluation rerun | **Yes** | **Yes** | Recommended |
| Notebook rerun (`notebooks/main.ipynb`) | **Yes** | **Yes** | Recommended |
| Research pack validation (`tools/evidence/validate_research_pack.py`) | No | No | No |
