# Evidence Validation Tool

## Purpose

`validate_research_pack.py` performs automated validation of the Waste Model
Release Evidence Pack. It checks file presence, content integrity, forbidden
phrase absence, and required phrase presence across `docs/research_pack/`.

The tool does not require the training dataset, TensorFlow model loading,
or internet access.

## Usage

```bash
python tools/evidence/validate_research_pack.py
```

Run from the repository root.

## What It Checks

- All required research pack files are present under `docs/research_pack/`
- The bundled checkpoint exists at `models/vgg16_waste_classifier.keras`
- `README.md` references `ACADEMIC_RESEARCH_BRIEF.md`
- `README.md` references the validation tool command
- Key output files exist (`outputs/evaluation_reports.txt`, etc.)
- Forbidden phrases are absent from all research pack documents
- Institution-specific wording is absent from research pack documents
- Required limitation phrases are present somewhere in the research pack
- `MODEL_RELEASE_CARD.md` documents the checkpoint path and SHA256 or file size
- `SUSTAINABILITY_USE_CASE_BOUNDARY.md` states impact is not measured
- `CALIBRATION_AND_THRESHOLDING_PROTOCOL.md` states no calibration results generated
- `INTERPRETABILITY_PROTOCOL.md` states no Grad-CAM/saliency/occlusion artifacts generated
- `METRIC_PROVENANCE_MATRIX.md` states no confusion matrix is claimed

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | All checks passed |
| 1 | One or more checks failed |

## Integration

Add to CI or pre-commit workflow:

```yaml
- name: Validate research pack
  run: python tools/evidence/validate_research_pack.py
```
