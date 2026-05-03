# Dataset and Task Card

## Task Name

Binary waste image classification — Organic (O) vs. Recyclable (R)

## Label Space

| Label | Symbol | Meaning |
|---|---|---|
| Organic | `O` | Organic waste items (food scraps, plant matter, biodegradable materials) |
| Recyclable | `R` | Recyclable waste items (plastics, metals, paper, glass) |

This is a strictly binary classification task. No intermediate or multi-class
labels are defined.

## Dataset Status

- The dataset is **not bundled** with this repository.
- The checkpoint is bundled at `models/vgg16_waste_classifier.keras` and is
  sufficient for single-image inference without the dataset.
- The dataset is required to reproduce training and evaluation results.

## Expected Local Dataset Layout

Before running the notebook or training scripts, place the dataset locally under:

```text
data/
└── o-vs-r-split/
    ├── train/
    │   ├── O/
    │   └── R/
    └── test/
        ├── O/
        └── R/
```

This structure is documented in `data/README.md`.

## Dataset Provenance

The `data/` directory is excluded from Git (see `.gitignore`). The preserved
notebook (`notebooks/main.ipynb`) contains an optional helper cell that can
download a reduced version of the dataset if the local folder is absent.
The dataset source and any applicable upstream terms of use are not reproduced
in this card; refer to the notebook and original dataset documentation for
provenance details.

## Recorded Generator Counts (from preserved notebook metadata)

| Split | Recorded image count |
|---|---|
| Training | 800 |
| Validation | 200 |
| Test | 200 |

The evaluation test set used for the preserved classification reports consists
of **100 held-out images: 50 Organic and 50 Recyclable** (confirmed from
the support column of `outputs/evaluation_reports.txt`).

The validation split was 0.2, and `steps_per_epoch` was set to 5 in the
preserved notebook run.

These counts are from stored notebook metadata. They reflect the session in
which the bundled checkpoint was produced. They are not independently verified
against the raw dataset in this pass.

## Binary Task Boundaries

This task is scoped to binary O/R classification only. It explicitly does not cover:

- **Multi-class waste taxonomy** — plastics, metals, glass, paper, cardboard,
  textiles, e-waste, hazardous waste, etc. are not individually labelled.
- **Material composition analysis** — the model classifies the visual
  appearance of an image, not the material properties of an object.
- **Contamination detection** — a recyclable item with food residue is not
  handled as a distinct class; it may be misclassified.
- **Multi-label classification** — images containing multiple items of
  different waste classes are not supported; one label is produced per image.
- **Degree of recyclability** — the model does not output a continuous
  measure of recyclability or compostability.
- **Real recycling facility validation** — the model has not been evaluated
  against images from operational sorting facilities.
- **Regulatory compliance** — classification outputs do not constitute legal
  or regulatory determination of waste category.

## Raw Sample Input Images

The repository intentionally does not include raw sample input images. This
is documented in `README.md` under Repository Notes. The `outputs/` directory
contains qualitative prediction example images from the notebook training
session; these are preserved artefacts, not raw dataset samples.

## Reproducibility Notes

| Task | Dataset required? | Notes |
|---|---|---|
| Single-image inference | No | Bundled checkpoint + `predict.py` sufficient |
| Unit tests (`pytest`) | No | Tests mock model loading; no dataset needed |
| Training notebook rerun | **Yes** | Requires dataset under `data/o-vs-r-split/` |
| Metric reproduction | **Yes** | Requires dataset and recorded TF 2.17.0 environment |
| Research pack validation | No | File-system and text checks only |

## Licensing and Provenance Notes

- Repository code is released under the MIT License (see `LICENSE`).
- Dataset usage is subject to the upstream data source terms. The dataset
  is not redistributed here.
- Model checkpoint weights incorporate ImageNet pre-training (VGG16).
  ImageNet model usage is subject to the original VGG16 licence terms from
  the Visual Geometry Group, University of Oxford.
