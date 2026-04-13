# Waste Classification using Transfer Learning (VGG16)

## Overview

This project builds an image classification workflow for waste sorting using transfer learning with `VGG16`. The goal is to classify waste images into two categories:

- `O`: Organic
- `R`: Recyclable

The notebook in [notebooks/main.ipynb](notebooks/main.ipynb) is the main source of truth for the project and contains the original training, fine-tuning, evaluation, and visual outputs.

## Key Results

- Fine-tuned test accuracy: `0.83`
- Best validation accuracy: `0.8854`
- Best validation loss: `0.2709`
- Input size: `150x150`
- Classes: `Organic (O)` and `Recyclable (R)`

![Fine-Tuned Accuracy Curve](outputs/fine_tuned_accuracy_curve.png)

## Model Availability

One trained checkpoint is currently included in this repository:

- `models/vgg16_waste_classifier.keras`

The dataset is still not bundled with the repository. The included model can be used directly with [predict.py](predict.py), while the notebook can still be rerun locally to regenerate checkpoints if needed.

## Business / Industrial Context

GreenCity is struggling with manual waste sorting, especially when recyclable and organic waste are mixed together. EcoClean needs an AI-based image classifier that can support smarter waste management, reduce contamination in recycling streams, and improve sorting efficiency.

## Approach

- Transfer learning with a pre-trained `VGG16` backbone (`include_top=False`, ImageNet weights)
- A custom binary classification head with dense and dropout layers
- Image preprocessing with `150x150` RGB inputs and `1/255` rescaling
- Data augmentation on the training split with horizontal flip and small width / height shifts
- Fine-tuning by unfreezing the last VGG16 convolution block starting from `block5_conv3`

## Notebook Facts Extracted From The Stored Run

- TensorFlow version: `2.17.0`
- Generator counts:
  - Training: `800` images
  - Validation: `200` images
  - Test: `200` images
- Input size: `150 x 150`
- Validation split: `0.2`
- Epochs configured in the notebook: `10`
- Training configuration kept from the source notebook: `steps_per_epoch=5`
- Frozen-backbone model summary:
  - Total params: `19,172,673`
  - Trainable params: `4,457,985`
  - Non-trainable params: `14,714,688`

## Results

The following numbers come from the stored notebook outputs only. They are not presented as a fresh rerun.

| Model | Test Accuracy | Organic (`O`) Precision / Recall | Recyclable (`R`) Precision / Recall | Best Validation Accuracy | Best Validation Loss |
| --- | --- | --- | --- | --- | --- |
| Extract-features VGG16 | `0.79` | `0.76 / 0.84` | `0.82 / 0.74` | `0.8802` | `0.3567` |
| Fine-tuned VGG16 | `0.83` | `0.80 / 0.88` | `0.87 / 0.78` | `0.8854` | `0.2709` |

Evaluation in the notebook is performed on `100` held-out test images loaded explicitly in the code (`50` organic and `50` recyclable).

## Visual Outputs

- Training curves:
  [Extract-features loss](outputs/extract_features_loss_curve.png),
  [Extract-features accuracy](outputs/extract_features_accuracy_curve.png),
  [Fine-tuned loss](outputs/fine_tuned_loss_curve.png),
  [Fine-tuned accuracy](outputs/fine_tuned_accuracy_curve.png)
- Evaluation artifacts:
  [Combined evaluation reports](outputs/evaluation_reports.txt),
  [Extract-features report](outputs/extract_features_classification_report.txt),
  [Fine-tuned report](outputs/fine_tuned_classification_report.txt)
- Qualitative examples:
  [Augmented training samples](outputs/augmented_organic_samples.png),
  [Extract-features prediction 0](outputs/extract_features_prediction_example_0.png),
  [Extract-features prediction 1](outputs/extract_features_prediction_example_1.png),
  [Fine-tuned prediction 1](outputs/fine_tuned_prediction_example_1.png)

## Project Structure

```text
waste-classification-transfer-learning/
+-- data/
|   +-- README.md
+-- models/
|   +-- vgg16_waste_classifier.keras
|   +-- .gitkeep
+-- notebooks/
|   +-- main.ipynb
+-- outputs/
|   +-- *.png
|   +-- *.txt
+-- .gitignore
+-- predict.py
+-- README.md
+-- requirements.txt
```

## Dataset

Place the dataset locally under `data/o-vs-r-split/` before running the notebook:

```text
data/
+-- o-vs-r-split/
    +-- train/
    |   +-- O/
    |   +-- R/
    +-- test/
        +-- O/
        +-- R/
```

The notebook also contains an optional helper cell that can download the same reduced dataset used in the original source notebook if the folder is missing.

## How to Run

1. `python -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Put the dataset inside `data/o-vs-r-split/`
5. Open and run [notebooks/main.ipynb](notebooks/main.ipynb)

## Quick Inference

The repository already includes a trained checkpoint at `models/vgg16_waste_classifier.keras`, so you can run inference directly:

```bash
python predict.py path\\to\\image.jpg
```

Optional:

```bash
python predict.py path\\to\\image.jpg --model models\\vgg16_waste_classifier.keras
```

By default, the script loads `models/vgg16_waste_classifier.keras`.

## Limitations

- The dataset is not included in the repository.
- The current project targets binary classification only: `Organic (O)` vs `Recyclable (R)`.
- Reported metrics are taken from stored notebook outputs already present in the project, not from a fresh rerun in this session.
- The bundled model file is relatively large for a standard Git repository.

## Notes

- The repository does not include the dataset.
- The trained checkpoint `models/vgg16_waste_classifier.keras` is included in the repository.
- Other local model files remain excluded from Git by default.
- The notebook was cleaned for portfolio / GitHub use, but the VGG16-based methodology was kept intact.
- A confusion matrix was not present in the source notebook outputs, so none is claimed here.
