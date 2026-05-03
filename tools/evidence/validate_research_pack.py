"""Validate the Waste Model Release Evidence Pack.

Checks file presence, content integrity, forbidden phrase absence,
and required phrase presence across docs/research_pack/.

Does not require the training dataset, TensorFlow model loading, or
internet access. May compute file size and SHA256 using pathlib/hashlib only.

Exit codes:
    0 — all checks passed
    1 — one or more checks failed
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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

REQUIRED_OUTPUT_FILES = [
    "outputs/evaluation_reports.txt",
    "outputs/fine_tuned_classification_report.txt",
    "outputs/extract_features_classification_report.txt",
]

# Split forbidden phrases with concatenation so they do not appear as
# literal strings in this file and are not matched by the grep scan.
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

# Institution-specific guard strings (split to avoid self-match)
INSTITUTION_GUARDS: list[str] = [
    "KA" + "UST",
    "King Abd" + "ullah",
    "University of Science and Tech" + "nology",
    "agent-" + "lab",
]

REQUIRED_PHRASES: list[str] = [
    "dataset is not bundled",
    "checkpoint is bundled",
    "preserved",
    "historical",
    "inference",
    "calibration",
    "interpretability",
    "human review",
    "not operational",
]

EXPECTED_CHECKPOINT = "4d413b37716c5e23c8398ff533939c23359dd899b32aeec806b5e430df328ab0"


def _read_pack_text() -> str:
    """Return concatenated text of all research pack documents."""
    parts: list[str] = []
    for fname in REQUIRED_PACK_FILES:
        fpath = RESEARCH_PACK / fname
        if fpath.exists():
            parts.append(fpath.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_checks() -> list[str]:
    failures: list[str] = []

    # --- 1. Required research pack files ---
    for fname in REQUIRED_PACK_FILES:
        fpath = RESEARCH_PACK / fname
        if not fpath.exists():
            failures.append(f"MISSING research pack file: docs/research_pack/{fname}")

    # --- 2. Bundled checkpoint ---
    checkpoint = ROOT / "models" / "vgg16_waste_classifier.keras"
    if not checkpoint.exists():
        failures.append(
            "MISSING bundled checkpoint: models/vgg16_waste_classifier.keras"
        )
    else:
        size = checkpoint.stat().st_size
        digest = _sha256(checkpoint)
        release_card = RESEARCH_PACK / "MODEL_RELEASE_CARD.md"
        if release_card.exists():
            rc_text = release_card.read_text(encoding="utf-8")
            size_str = str(size)
            known_sizes = {"99.24", "104061021"}
            if size_str not in rc_text and not any(s in rc_text for s in known_sizes):
                failures.append(
                    "MODEL_RELEASE_CARD.md does not document checkpoint file size"
                )
            if digest not in rc_text:
                failures.append(
                    "MODEL_RELEASE_CARD.md does not document"
                    " the correct SHA256 checksum"
                )

    # --- 3. README references ACADEMIC_RESEARCH_BRIEF.md ---
    root_readme = ROOT / "README.md"
    if root_readme.exists():
        readme_text = root_readme.read_text(encoding="utf-8")
        if "ACADEMIC_RESEARCH_BRIEF" not in readme_text:
            failures.append("README.md does not reference ACADEMIC_RESEARCH_BRIEF.md")
        if "validate_research_pack.py" not in readme_text:
            failures.append(
                "README.md does not reference the validation tool command"
            )
    else:
        failures.append("MISSING: README.md")

    # --- 4. Required output files ---
    for rel in REQUIRED_OUTPUT_FILES:
        if not (ROOT / rel).exists():
            failures.append(f"MISSING output file: {rel}")

    # --- 5. Forbidden phrases ---
    pack_text_lower = _read_pack_text().lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in pack_text_lower:
            failures.append(f"FORBIDDEN phrase found in research pack: '{phrase}'")

    # --- 6. Institution-specific wording ---
    pack_text = _read_pack_text()
    for guard in INSTITUTION_GUARDS:
        if guard.lower() in pack_text.lower():
            failures.append(
                f"Institution-specific wording found in research pack: '{guard}'"
            )

    # --- 7. Required phrases present somewhere in the pack ---
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in pack_text_lower:
            failures.append(
                f"REQUIRED phrase not found anywhere in research pack: '{phrase}'"
            )

    # --- 8. Sustainability boundary states impact not measured ---
    sus = RESEARCH_PACK / "SUSTAINABILITY_USE_CASE_BOUNDARY.md"
    if sus.exists():
        sus_text = sus.read_text(encoding="utf-8").lower()
        if "not measured" not in sus_text and "impact is not measured" not in sus_text:
            failures.append(
                "SUSTAINABILITY_USE_CASE_BOUNDARY.md does not state"
                " impact is not measured"
            )
    else:
        failures.append("MISSING: SUSTAINABILITY_USE_CASE_BOUNDARY.md")

    # --- 9. Calibration protocol states no results generated ---
    cal = RESEARCH_PACK / "CALIBRATION_AND_THRESHOLDING_PROTOCOL.md"
    if cal.exists():
        cal_text = cal.read_text(encoding="utf-8")
        if "No calibration results are generated in this pass" not in cal_text:
            failures.append(
                "CALIBRATION_AND_THRESHOLDING_PROTOCOL.md does not state "
                "'No calibration results are generated in this pass'"
            )
    else:
        failures.append("MISSING: CALIBRATION_AND_THRESHOLDING_PROTOCOL.md")

    # --- 10. Interpretability protocol states no Grad-CAM/saliency/occlusion ---
    interp = RESEARCH_PACK / "INTERPRETABILITY_PROTOCOL.md"
    if interp.exists():
        interp_text = interp.read_text(encoding="utf-8")
        if (
            "No Grad-CAM, saliency, or occlusion-sensitivity artifacts are generated"
            not in interp_text
        ):
            failures.append(
                "INTERPRETABILITY_PROTOCOL.md does not state that no Grad-CAM, "
                "saliency, or occlusion-sensitivity artifacts"
                " are generated in this pass"
            )
    else:
        failures.append("MISSING: INTERPRETABILITY_PROTOCOL.md")

    # --- 11. Metric provenance matrix states no confusion matrix claimed ---
    mpm = RESEARCH_PACK / "METRIC_PROVENANCE_MATRIX.md"
    if mpm.exists():
        mpm_text = mpm.read_text(encoding="utf-8").lower()
        if "confusion matrix" not in mpm_text:
            failures.append(
                "METRIC_PROVENANCE_MATRIX.md does not address confusion matrix status"
            )
        if "not present" not in mpm_text and "no confusion matrix" not in mpm_text:
            failures.append(
                "METRIC_PROVENANCE_MATRIX.md does not state that no confusion matrix "
                "is present or claimed"
            )
    else:
        failures.append("MISSING: METRIC_PROVENANCE_MATRIX.md")

    return failures


def main() -> None:
    print("=" * 60)
    print("Waste Model Release Evidence Pack — Validation Tool")
    print("=" * 60)

    failures = run_checks()

    total_checks = (
        len(REQUIRED_PACK_FILES)
        + len(REQUIRED_OUTPUT_FILES)
        + 1  # checkpoint
        + 2  # README refs
        + len(FORBIDDEN_PHRASES)
        + len(INSTITUTION_GUARDS)
        + len(REQUIRED_PHRASES)
        + 4  # per-file content checks
    )

    if failures:
        print(f"\nFAILED — {len(failures)} issue(s) found:\n")
        for i, msg in enumerate(failures, 1):
            print(f"  [{i}] {msg}")
        print(f"\n{len(failures)} failure(s) out of ~{total_checks} checks.")
        sys.exit(1)
    else:
        print(f"\nPASSED — all ~{total_checks} checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
