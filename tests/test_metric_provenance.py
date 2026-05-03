"""Tests verifying metric provenance in the research pack documentation.

Checks that preserved metrics from README.md and output text files are
referenced in METRIC_PROVENANCE_MATRIX.md, and that forbidden wording
is absent.

These tests do not require the training dataset, TensorFlow model loading,
or internet access.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_PACK = ROOT / "docs" / "research_pack"
MPM = RESEARCH_PACK / "METRIC_PROVENANCE_MATRIX.md"


def _mpm_text() -> str:
    assert MPM.exists(), "METRIC_PROVENANCE_MATRIX.md is missing"
    return MPM.read_text(encoding="utf-8")


# Metrics that must be referenced in the provenance matrix
REQUIRED_METRIC_REFERENCES: list[tuple[str, str]] = [
    ("0.83", "fine-tuned test accuracy 0.83"),
    ("0.8854", "best validation accuracy 0.8854"),
    ("0.2709", "best validation loss 0.2709"),
    ("0.79", "extract-features test accuracy 0.79"),
    ("0.80", "fine-tuned Organic precision 0.80"),
    ("0.88", "fine-tuned Organic recall 0.88"),
    ("0.87", "fine-tuned Recyclable precision 0.87"),
    ("0.78", "fine-tuned Recyclable recall 0.78"),
    ("0.76", "extract-features Organic precision 0.76"),
    ("0.84", "extract-features Organic recall 0.84"),
    ("0.82", "extract-features Recyclable precision 0.82"),
    ("0.74", "extract-features Recyclable recall 0.74"),
    ("150", "input size 150x150"),
    ("2.17.0", "TensorFlow version 2.17.0"),
    ("100", "test set size 100 images"),
]


@pytest.mark.parametrize("value,description", REQUIRED_METRIC_REFERENCES)
def test_metric_value_referenced_in_provenance_matrix(
    value: str, description: str
) -> None:
    text = _mpm_text()
    assert value in text, (
        f"METRIC_PROVENANCE_MATRIX.md does not reference {description} (value: {value})"
    )


def test_provenance_matrix_states_no_confusion_matrix() -> None:
    text = _mpm_text().lower()
    assert "confusion matrix" in text, (
        "METRIC_PROVENANCE_MATRIX.md does not address confusion matrix status"
    )
    assert "not present" in text or "no confusion matrix" in text, (
        "METRIC_PROVENANCE_MATRIX.md does not state that no confusion matrix "
        "is present or claimed"
    )


def test_provenance_matrix_states_metrics_are_preserved() -> None:
    text = _mpm_text().lower()
    assert "preserved" in text, (
        "METRIC_PROVENANCE_MATRIX.md does not state that metrics are preserved "
        "historical artifacts"
    )


def test_provenance_matrix_states_no_fresh_reproduction() -> None:
    text = _mpm_text().lower()
    assert "not newly reproduced" in text or "newly reproduced" in text, (
        "METRIC_PROVENANCE_MATRIX.md should address whether metrics were "
        "newly reproduced"
    )


def test_provenance_matrix_states_no_calibrated_probabilities() -> None:
    text = _mpm_text().lower()
    assert "calibrat" in text, (
        "METRIC_PROVENANCE_MATRIX.md does not mention calibration caveats"
    )


def test_output_files_referenced_in_provenance_matrix() -> None:
    text = _mpm_text()
    assert "fine_tuned_classification_report.txt" in text, (
        "METRIC_PROVENANCE_MATRIX.md does not reference "
        "fine_tuned_classification_report.txt"
    )
    assert "extract_features_classification_report.txt" in text, (
        "METRIC_PROVENANCE_MATRIX.md does not reference "
        "extract_features_classification_report.txt"
    )
    assert "evaluation_reports.txt" in text, (
        "METRIC_PROVENANCE_MATRIX.md does not reference evaluation_reports.txt"
    )


def test_output_files_values_match_stored_reports() -> None:
    """Spot-check that values in output files match what provenance matrix claims."""
    fine_report = ROOT / "outputs" / "fine_tuned_classification_report.txt"
    extract_report = ROOT / "outputs" / "extract_features_classification_report.txt"

    if fine_report.exists():
        text = fine_report.read_text(encoding="utf-8")
        assert "0.83" in text, (
            "fine_tuned_classification_report.txt does not contain 0.83"
        )
        assert "0.80" in text, (
            "fine_tuned_classification_report.txt does not contain 0.80"
        )
        assert "0.87" in text, (
            "fine_tuned_classification_report.txt does not contain 0.87"
        )

    if extract_report.exists():
        text = extract_report.read_text(encoding="utf-8")
        assert "0.79" in text, (
            "extract_features_classification_report.txt does not contain 0.79"
        )
        assert "0.76" in text, (
            "extract_features_classification_report.txt does not contain 0.76"
        )
        assert "0.82" in text, (
            "extract_features_classification_report.txt does not contain 0.82"
        )


def test_no_forbidden_phrases_in_provenance_matrix() -> None:
    text = _mpm_text().lower()
    forbidden = [
        "state-of-the-" + "art",
        "production recycling " + "system",
        "industrial " + "validation",
        "guaranteed sorting " + "accuracy",
        "measured environmental " + "impact",
        "operational recycling " + "facility",
    ]
    for phrase in forbidden:
        assert phrase.lower() not in text, (
            f"Forbidden phrase found in METRIC_PROVENANCE_MATRIX.md: '{phrase}'"
        )
