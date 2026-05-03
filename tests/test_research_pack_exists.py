"""Tests verifying the Waste Model Release Evidence Pack files exist and
are free of forbidden content.

These tests do not require the training dataset, TensorFlow model loading,
or internet access.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_PACK = ROOT / "docs" / "research_pack"

REQUIRED_PACK_FILES = [
    "README.md",
    "ACADEMIC_RESEARCH_BRIEF.md",
    "MODEL_CARD.md",
    "MODEL_RELEASE_CARD.md",
    "CHECKPOINT_AND_INFERENCE_CARD.md",
    "METRIC_PROVENANCE_MATRIX.md",
    "DATASET_AND_TASK_CARD.md",
    "SUSTAINABILITY_USE_CASE_BOUNDARY.md",
    "FAILURE_MODE_MATRIX.md",
    "CALIBRATION_AND_THRESHOLDING_PROTOCOL.md",
    "INTERPRETABILITY_PROTOCOL.md",
    "INFERENCE_REPRODUCIBILITY_GUIDE.md",
    "REPRODUCIBILITY_CHECKLIST.md",
]

# Forbidden phrases split to avoid self-match in grep scans
FORBIDDEN_PHRASES: list[str] = [
    "state-of-the-" + "art",
    "production recycling " + "system",
    "industrial " + "validation",
    "validated waste sorting " + "deployment",
    "guaranteed sorting " + "accuracy",
    "measured environmental " + "impact",
    "operational recycling " + "facility",
    "fully automated waste management " + "system",
]

INSTITUTION_GUARDS: list[str] = [
    "KA" + "UST",
    "King Abd" + "ullah",
    "University of Science and Tech" + "nology",
    "agent-" + "lab",
]


@pytest.mark.parametrize("filename", REQUIRED_PACK_FILES)
def test_research_pack_file_exists(filename: str) -> None:
    fpath = RESEARCH_PACK / filename
    assert fpath.exists(), f"Missing research pack file: docs/research_pack/{filename}"


def test_bundled_checkpoint_exists() -> None:
    checkpoint = ROOT / "models" / "vgg16_waste_classifier.keras"
    assert checkpoint.exists(), (
        "Bundled checkpoint not found: models/vgg16_waste_classifier.keras"
    )


def test_readme_references_academic_research_brief() -> None:
    readme = ROOT / "README.md"
    assert readme.exists(), "README.md is missing"
    text = readme.read_text(encoding="utf-8")
    assert "ACADEMIC_RESEARCH_BRIEF" in text, (
        "README.md does not reference ACADEMIC_RESEARCH_BRIEF.md"
    )


def test_readme_references_validation_tool() -> None:
    readme = ROOT / "README.md"
    assert readme.exists(), "README.md is missing"
    text = readme.read_text(encoding="utf-8")
    assert "validate_research_pack.py" in text, (
        "README.md does not reference the validation tool command"
    )


def _read_pack_text() -> str:
    parts: list[str] = []
    for fname in REQUIRED_PACK_FILES:
        fpath = RESEARCH_PACK / fname
        if fpath.exists():
            parts.append(fpath.read_text(encoding="utf-8"))
    return "\n".join(parts)


@pytest.mark.parametrize("phrase", FORBIDDEN_PHRASES)
def test_forbidden_phrase_absent(phrase: str) -> None:
    pack_text = _read_pack_text().lower()
    assert phrase.lower() not in pack_text, (
        f"Forbidden phrase found in research pack: '{phrase}'"
    )


@pytest.mark.parametrize("guard", INSTITUTION_GUARDS)
def test_no_institution_specific_wording(guard: str) -> None:
    pack_text = _read_pack_text().lower()
    assert guard.lower() not in pack_text, (
        f"Institution-specific wording found in research pack: '{guard}'"
    )


def test_model_release_card_documents_checkpoint_path() -> None:
    rc = RESEARCH_PACK / "MODEL_RELEASE_CARD.md"
    assert rc.exists()
    text = rc.read_text(encoding="utf-8")
    assert "vgg16_waste_classifier.keras" in text, (
        "MODEL_RELEASE_CARD.md does not document the checkpoint path"
    )


def test_model_release_card_documents_checksum_or_size() -> None:
    rc = RESEARCH_PACK / "MODEL_RELEASE_CARD.md"
    assert rc.exists()
    text = rc.read_text(encoding="utf-8")
    has_sha = "4d413b37716c5e23c8398ff533939c23359dd899b32aeec806b5e430df328ab0" in text
    has_size = "104061021" in text or "99.24" in text
    assert has_sha or has_size, (
        "MODEL_RELEASE_CARD.md does not document checkpoint SHA256 or file size"
    )


def test_sustainability_boundary_states_impact_not_measured() -> None:
    sus = RESEARCH_PACK / "SUSTAINABILITY_USE_CASE_BOUNDARY.md"
    assert sus.exists()
    text = sus.read_text(encoding="utf-8").lower()
    assert "not measured" in text or "impact is not measured" in text, (
        "SUSTAINABILITY_USE_CASE_BOUNDARY.md does not state impact is not measured"
    )


def test_calibration_protocol_states_no_results_generated() -> None:
    cal = RESEARCH_PACK / "CALIBRATION_AND_THRESHOLDING_PROTOCOL.md"
    assert cal.exists()
    text = cal.read_text(encoding="utf-8")
    assert "No calibration results are generated in this pass" in text, (
        "CALIBRATION_AND_THRESHOLDING_PROTOCOL.md must state "
        "'No calibration results are generated in this pass'"
    )


def test_interpretability_protocol_states_no_gradcam_generated() -> None:
    interp = RESEARCH_PACK / "INTERPRETABILITY_PROTOCOL.md"
    assert interp.exists()
    text = interp.read_text(encoding="utf-8")
    assert (
        "No Grad-CAM, saliency, or occlusion-sensitivity artifacts are generated"
        in text
    ), (
        "INTERPRETABILITY_PROTOCOL.md must state that no Grad-CAM, saliency, "
        "or occlusion-sensitivity artifacts are generated in this pass"
    )


def test_validation_tool_passes() -> None:
    result = subprocess.run(
        [sys.executable, "tools/evidence/validate_research_pack.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"validate_research_pack.py failed:\n{result.stdout}\n{result.stderr}"
    )
