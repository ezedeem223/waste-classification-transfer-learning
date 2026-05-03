# Metric Provenance Matrix

All metrics documented here are **preserved historical evaluation artifacts**
sourced from stored notebook outputs. None were newly reproduced or recomputed
in this documentation pass. The dataset used to generate these metrics is not
bundled in this repository.

## Red Lines

- Do not call these metrics newly reproduced unless rerun commands were actually executed with the dataset.
- Do not present these metrics as validation against industrial systems.
- Do not imply any quantified environmental impact.
- Do not imply real-world recycling stream robustness.
- Do not imply broad object or material generalisation.
- Do not invent confusion matrix metrics. No confusion matrix artifact is present in this repository.
- Do not claim calibrated probabilities without calibration analysis.

---

## Metric Provenance Table

| Metric | Value | Source File | Source Context | Evidence Confidence | Allowed Wording | Forbidden Wording |
|---|---|---|---|---|---|---|
| Fine-tuned test accuracy | 0.83 | `outputs/fine_tuned_classification_report.txt`, `outputs/evaluation_reports.txt`, `README.md` | Accuracy row, 100-sample test set | High — consistent across three sources | "preserved test accuracy", "stored notebook output" | "validated accuracy", "production accuracy", "guaranteed accuracy" |
| Fine-tuned best validation accuracy | 0.8854 | `README.md` | Key Results section and Results table | Medium — from README summary; original notebook cell not separately verified in this pass | "best validation accuracy from stored notebook output" | "reproduced validation accuracy", "confirmed via fresh run" |
| Fine-tuned best validation loss | 0.2709 | `README.md` | Key Results section and Results table | Medium — same as above | "best validation loss from stored notebook output" | "reproduced validation loss" |
| Fine-tuned Organic (O) precision | 0.80 | `outputs/fine_tuned_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, O row | High — present in output files | "preserved precision for Organic class" | "guaranteed precision", "production precision" |
| Fine-tuned Organic (O) recall | 0.88 | `outputs/fine_tuned_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, O row | High | "preserved recall for Organic class" | "guaranteed recall" |
| Fine-tuned Organic (O) F1-score | 0.84 | `outputs/fine_tuned_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, O row | High | "preserved F1 for Organic class" | "guaranteed F1" |
| Fine-tuned Recyclable (R) precision | 0.87 | `outputs/fine_tuned_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, R row | High | "preserved precision for Recyclable class" | "guaranteed precision" |
| Fine-tuned Recyclable (R) recall | 0.78 | `outputs/fine_tuned_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, R row | High | "preserved recall for Recyclable class" | "guaranteed recall" |
| Fine-tuned Recyclable (R) F1-score | 0.82 | `outputs/fine_tuned_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, R row | High | "preserved F1 for Recyclable class" | "guaranteed F1" |
| Extract-features test accuracy | 0.79 | `outputs/extract_features_classification_report.txt`, `outputs/evaluation_reports.txt`, `README.md` | Accuracy row, 100-sample test set | High — consistent across three sources | "preserved extract-features test accuracy" | "validated accuracy" |
| Extract-features best validation accuracy | 0.8802 | `README.md` | Results table | Medium — from README summary | "best validation accuracy from stored notebook output" | "reproduced validation accuracy" |
| Extract-features best validation loss | 0.3567 | `README.md` | Results table | Medium — from README summary | "best validation loss from stored notebook output" | "reproduced validation loss" |
| Extract-features Organic (O) precision | 0.76 | `outputs/extract_features_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, O row | High | "preserved precision for Organic class (extract-features model)" | "guaranteed precision" |
| Extract-features Organic (O) recall | 0.84 | `outputs/extract_features_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, O row | High | "preserved recall for Organic class (extract-features model)" | "guaranteed recall" |
| Extract-features Recyclable (R) precision | 0.82 | `outputs/extract_features_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, R row | High | "preserved precision for Recyclable class (extract-features model)" | "guaranteed precision" |
| Extract-features Recyclable (R) recall | 0.74 | `outputs/extract_features_classification_report.txt`, `outputs/evaluation_reports.txt` | Classification report, R row | High | "preserved recall for Recyclable class (extract-features model)" | "guaranteed recall" |
| Training generator count | 800 images | `README.md` | Stored Run Metadata section | Medium — from README summary of notebook | "recorded training image count from notebook metadata" | "verified dataset size" |
| Validation generator count | 200 images | `README.md` | Stored Run Metadata section | Medium — from README summary | "recorded validation image count" | "verified validation count" |
| Test generator count | 200 images | `README.md` | Stored Run Metadata section | Medium — from README summary | "recorded test generator count" | "verified test count" |
| Evaluation test set size | 100 images (50 O + 50 R) | `outputs/evaluation_reports.txt` (support column: 50 per class) | Support column confirms 50 O and 50 R | High — support column directly verifiable | "held-out evaluation test set of 100 images, 50 per class" | "full dataset evaluation" |
| Input size | 150 × 150 | `predict.py` (`IMAGE_SIZE = (150, 150)`), `README.md` | Code constant and documentation | High — verified in code | "input image size 150 × 150 pixels" | "arbitrary resolution input" |
| TensorFlow version | 2.17.0 | `requirements.txt`, `README.md` | Pinned dependency and Stored Run Metadata | High — pinned in requirements | "TensorFlow 2.17.0 (recorded training environment)" | "current TensorFlow version", "latest TF" |
| Validation split | 0.2 | `README.md` | Stored Run Metadata section | Medium — from README summary | "validation split of 0.2 from stored metadata" | "confirmed split" |
| Steps per epoch | 5 | `README.md` | Stored Run Metadata section | Medium — from README summary | "steps_per_epoch=5 from stored notebook metadata" | "standard steps per epoch" |
| Epochs configured | 10 | `README.md` | Stored Run Metadata section | Medium — from README summary | "10 epochs as configured in notebook" | "converged at 10 epochs" |
| Confusion matrix | Not present | — | Not found in any output file or notebook export | N/A — absence confirmed | "no confusion matrix is present or claimed" | Any claim of confusion matrix values |

---

## Evidence Confidence Levels

| Level | Meaning |
|---|---|
| High | Metric appears verbatim in one or more committed output files and is cross-verifiable |
| Medium | Metric appears in README summary or notebook metadata; not independently verified against raw notebook cell output in this pass |
| N/A (absence) | Artifact confirmed absent; no value can be stated |

---

## Summary Statement

All metrics in this matrix are preserved from the original training session.
No metric was computed by running evaluation commands in this documentation
pass. Reproduction of these metrics requires the original dataset, the recorded
TF 2.17.0 environment, and the steps documented in `notebooks/main.ipynb`.
