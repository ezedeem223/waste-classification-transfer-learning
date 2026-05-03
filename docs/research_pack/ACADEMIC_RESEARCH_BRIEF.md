# Academic Research Brief

## 1. Problem Definition

Manual sorting of mixed waste streams is labour-intensive, error-prone, and
inconsistent across facilities and operators. Automated image-based classification
represents one potential component in AI-assisted waste management pipelines.
This repository documents a transfer-learning baseline for binary waste image
classification: distinguishing **Organic (O)** from **Recyclable (R)** waste
items from single photographic images.

## 2. Why Visual Waste Classification Matters

Misclassification of waste at the point of sorting degrades recycling stream
purity, increases downstream contamination handling costs, and reduces the
fraction of material that enters closed-loop recycling. Sustainability-oriented
computer vision research explores whether off-the-shelf image representations
can provide a reliable low-cost signal for initial triage.

Binary classification — the simplest non-trivial formulation of this problem —
provides a reproducible baseline against which more complex multi-class,
multi-label, or material-composition approaches can be compared.

## 3. Task Scope

- **Task type:** Binary supervised image classification
- **Label space:** `O` (Organic), `R` (Recyclable)
- **Input:** Single RGB image, resized to 150 × 150 pixels
- **Preprocessing:** Pixel values rescaled to [0, 1] by dividing by 255
- **Output:** A single scalar `recyclable_probability` ∈ [0, 1];
  `organic_probability = 1 − recyclable_probability`
- **Decision boundary:** Default threshold of 0.5 applied in `predict.py`

This scope deliberately excludes:
- Multi-class waste taxonomy (plastics, metals, glass, paper, etc.)
- Material composition analysis
- Contamination detection (e.g. recyclable with food residue)
- Real-time video classification
- Facility-level sorting validation

## 4. Transfer-Learning Approach

The classifier uses a **VGG16** convolutional backbone pre-trained on ImageNet,
with the top classification layers removed (`include_top=False`). A custom binary
classification head with dense and dropout layers is attached and trained on the
waste dataset.

Two training phases are documented in the preserved notebook:

1. **Extract-features phase:** VGG16 backbone frozen; only the custom head is
   trained. Reported test accuracy: 0.79.
2. **Fine-tuning phase:** VGG16 layers from `block5_conv3` onward are unfrozen
   and trained at a lower learning rate alongside the head. Reported test
   accuracy: 0.83.

The bundled checkpoint (`models/vgg16_waste_classifier.keras`) corresponds to
the fine-tuned model.

All metric values cited above are **preserved historical evaluation artifacts**
taken from stored notebook outputs. They are not newly reproduced in this pass.

## 5. VGG16 Classifier Role

VGG16 serves as a general-purpose visual feature extractor. Its ImageNet
pre-training provides low- and mid-level visual features (edges, textures,
colour gradients) that transfer to the waste classification domain without
requiring full training from scratch. This reduces the volume of labelled waste
images needed to achieve reasonable performance.

The transferred features are not specifically adapted to waste material
properties; fine-tuning of the final convolutional block partially addresses
this limitation.

## 6. Maintained Inference Path

The file `predict.py` is the maintained, documented entry point for running
inference with the bundled checkpoint. It requires only the runtime dependencies
listed in `requirements.txt` and does not require the training dataset.

## 7. Bundled Checkpoint Role

`models/vgg16_waste_classifier.keras` is the primary model-release artifact of
this repository. It allows reviewers, researchers, and downstream users to:

- Verify that inference produces consistent outputs for a given input
- Explore the model's behaviour on new waste images
- Compare outputs against the preserved evaluation artifacts
- Use the checkpoint as a baseline in future comparative studies

The checkpoint does **not** guarantee:
- Performance on images from domains different from the training distribution
- Calibrated probability outputs
- Suitability for any operational sorting context

## 8. Current Evidence Artifacts

The following artifacts are preserved in this repository and constitute the
evidence base for the documented metrics:

| Artifact | Path | Role |
|---|---|---|
| Combined evaluation report | `outputs/evaluation_reports.txt` | Per-class precision/recall/F1 for both models |
| Extract-features report | `outputs/extract_features_classification_report.txt` | Detailed extract-features classification report |
| Fine-tuned report | `outputs/fine_tuned_classification_report.txt` | Detailed fine-tuned classification report |
| Training curves (PNG) | `outputs/*.png` | Visual loss/accuracy history |
| Prediction examples (PNG) | `outputs/*_prediction_example_*.png` | Qualitative example outputs |
| Augmented samples (PNG) | `outputs/augmented_organic_samples.png` | Training augmentation illustration |
| Preserved notebook | `notebooks/main.ipynb` | Original training and evaluation notebook |

No confusion matrix artifact is present or claimed in this repository.

## 9. Provenance Caveats

- All metrics are sourced from stored notebook outputs. No fresh evaluation run
  was executed in producing this evidence pack.
- The dataset used during training is not bundled; only the checkpoint is
  bundled.
- Generator counts (800 training, 200 validation, 200 test images) and the
  evaluation test set size (100 held-out images: 50 organic, 50 recyclable)
  are taken from the stored notebook and README.
- The TensorFlow version recorded in the notebook environment was 2.17.0.
- Validation accuracy (best: 0.8854) and validation loss (best: 0.2709) are
  preserved from notebook outputs and may reflect the best checkpoint seen
  during training, not necessarily the final epoch.

## 10. Methodological Risks

- **Small dataset:** 800 training images is a modest corpus. Performance
  generalisation to unseen waste image distributions is not guaranteed.
- **Binary simplification:** The two-class formulation does not capture the
  full complexity of real waste taxonomy.
- **Domain shift:** The training distribution is a curated dataset split; real
  facility images may differ substantially in lighting, angle, occlusion, and
  background.
- **Default threshold:** The 0.5 threshold is not optimised for any specific
  precision/recall trade-off. Downstream applications may require threshold
  adjustment.
- **Probability calibration:** The raw output probabilities are not verified
  to be calibrated. They should not be treated as well-calibrated confidence
  scores without further calibration analysis.
- **No adversarial robustness testing:** The model has not been evaluated
  against adversarial inputs or distribution shift stress tests.

## 11. Future Academic Research Directions

- Multi-class waste taxonomy beyond binary O/R
- Material composition classification (plastic type, metal grade)
- Contamination detection within otherwise recyclable items
- Domain adaptation from curated dataset images to real facility images
- Probability calibration study (Platt scaling, temperature scaling)
- Grad-CAM / saliency analysis to understand activated image regions
- Threshold optimisation for asymmetric cost functions (false recyclable vs.
  false organic)
- Dataset augmentation studies with controlled distribution shift
- Comparison against lighter architectures (MobileNet, EfficientNet-Lite)
  for edge deployment feasibility
- Multi-label classification to handle mixed-waste images
