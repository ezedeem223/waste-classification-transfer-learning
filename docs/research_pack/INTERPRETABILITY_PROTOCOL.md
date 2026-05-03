# Interpretability Protocol

## Important Statement

**No Grad-CAM, saliency, or occlusion-sensitivity artifacts are generated in this pass.**

No visual explanation outputs were produced in this documentation pass.
The dataset is not bundled; TensorFlow model loading for gradient-based
methods was not performed; and no interpretability artifacts are fabricated.

---

## What Visual Artifacts Currently Exist

The following output artifacts are preserved in this repository from the
original notebook training session:

| Artifact | Path | What It Shows |
|---|---|---|
| Extract-features loss curve | `outputs/extract_features_loss_curve.png` | Training and validation loss over epochs (extract-features phase) |
| Extract-features accuracy curve | `outputs/extract_features_accuracy_curve.png` | Training and validation accuracy over epochs (extract-features phase) |
| Fine-tuned loss curve | `outputs/fine_tuned_loss_curve.png` | Training and validation loss over epochs (fine-tuning phase) |
| Fine-tuned accuracy curve | `outputs/fine_tuned_accuracy_curve.png` | Training and validation accuracy over epochs (fine-tuning phase) |
| Augmented organic samples | `outputs/augmented_organic_samples.png` | Example images after training augmentation (horizontal flip, shift) |
| Extract-features prediction example 0 | `outputs/extract_features_prediction_example_0.png` | Qualitative prediction example from extract-features model |
| Extract-features prediction example 1 | `outputs/extract_features_prediction_example_1.png` | Qualitative prediction example from extract-features model |
| Fine-tuned prediction example 1 | `outputs/fine_tuned_prediction_example_1.png` | Qualitative prediction example from fine-tuned model |

These are preserved historical outputs. They were not regenerated in this
documentation pass.

---

## What Training Curves Can and Cannot Say

### Can Say

- Whether training loss decreased over epochs (model was learning)
- Whether a gap between training and validation curves is present (potential overfitting)
- At which epoch the best validation accuracy / lowest validation loss was achieved
- Whether the fine-tuning phase improved over the extract-features phase

### Cannot Say

- Which image regions the model uses to make decisions
- Whether the model is using task-relevant features (e.g. object texture vs. background)
- How the model would behave on out-of-distribution images
- Whether the model is robust to spurious correlations in the training set

Training curves are a measure of optimisation progress, not of
decision-process interpretability.

---

## Grad-CAM Protocol for VGG16

Grad-CAM (Gradient-weighted Class Activation Mapping) generates a heatmap
highlighting which spatial regions of the input image most influenced the
predicted class score.

**Protocol for future implementation (not executed in this pass):**

1. Load the bundled checkpoint using `tf.keras.models.load_model`.
2. Identify the target convolutional layer. For VGG16, the standard choice
   is the last convolutional layer: `block5_conv3`.
3. Use `tf.GradientTape` to compute gradients of the predicted class score
   with respect to the activations of `block5_conv3`.
4. Pool the gradients spatially (global average pooling over the spatial dims).
5. Weight the activation maps by the pooled gradients.
6. Apply ReLU to retain only positive influences.
7. Resize the heatmap to the input image size (150 × 150) and overlay on
   the original image.

**Expected output naming convention:**

```
outputs/gradcam_organic_example_{n}.png
outputs/gradcam_recyclable_example_{n}.png
outputs/gradcam_borderline_example_{n}.png
```

**Requirements:** Dataset image(s) or new sample image(s), TensorFlow 2.17.0,
matplotlib. No Grad-CAM outputs are present in this repository.

---

## Occlusion Sensitivity Protocol

Occlusion sensitivity systematically masks regions of the input image and
measures how the prediction probability changes. High sensitivity in a region
indicates the model relies on that region.

**Protocol for future implementation (not executed in this pass):**

1. Define a sliding window of size s × s pixels (e.g. 30 × 30) and stride d.
2. For each window position, replace the covered pixels with a constant value
   (e.g. 0 or the mean pixel value).
3. Run `predict.py` (or `predict_image`) on the modified image.
4. Record the change in `recyclable_probability` relative to the unmodified image.
5. Build a sensitivity heatmap from the per-position probability differences.
6. Overlay on the original image.

**Requirements:** Dataset image(s) or new sample image(s), Python, `predict.py`.
No occlusion sensitivity outputs are present in this repository.

---

## Saliency Map Caveats

Simple gradient-based saliency maps (vanilla backpropagation) are available
without the dataset (only a single input image is needed), but:

- Vanilla saliency maps are sensitive to noise and may not highlight
  semantically meaningful regions.
- Guided backpropagation variants are more visually coherent but may reflect
  artefacts of the ReLU gating rather than true class-relevant features.
- No saliency maps are generated in this pass.
- Saliency maps should not be presented as causal explanations.

---

## Example Naming Conventions for Future Outputs

| Output type | Naming pattern |
|---|---|
| Grad-CAM | `outputs/gradcam_{class}_{split}_example_{n}.png` |
| Occlusion sensitivity | `outputs/occlusion_{class}_{split}_example_{n}.png` |
| Saliency map | `outputs/saliency_{class}_{split}_example_{n}.png` |
| Integrated gradients | `outputs/integrated_gradients_{class}_{split}_example_{n}.png` |

Use `class` ∈ `{organic, recyclable}`, `split` ∈ `{train, val, test}`.

---

## Reviewer Caveats

- Interpretability visualisations show which image regions influenced the
  prediction for a **specific input**. They do not generalise across all
  inputs without aggregated analysis.
- A visually plausible heatmap (e.g. highlighting the object rather than the
  background) is encouraging but does not prove the model is using
  task-relevant features for the right reasons.
- A heatmap highlighting the background is a warning sign of spurious
  correlation but does not by itself quantify the performance impact.
- Interpretability tools are diagnostic aids, not proof of model correctness
  or fairness.

---

## No Causal Claims

Interpretability outputs from this model must not be used to make causal
claims. For example:

- "The model classifies this item as organic **because** it has a brown surface"
  is not supported by a Grad-CAM heatmap. The heatmap shows correlation between
  image regions and prediction, not causation.
- Classification correctness on a test set does not imply that the model has
  learned a causally valid representation of waste category.

---

## Summary

No interpretability artifacts are generated in this documentation pass.
The existing preserved outputs (training curves, qualitative prediction
examples) document training dynamics and example model behaviour, not
spatial decision-making. Future interpretability work should follow the
Grad-CAM, occlusion, and saliency protocols described above and adhere to
the naming conventions and reviewer caveats documented here.
