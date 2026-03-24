from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_bundle_validates() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "validate_bundle.py"),
            "--bundle",
            str(ROOT / "bundles" / "math_paper_llm_auditor.bundle.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr

def test_rulesets_validate() -> None:
    for rel in [
        "rules/knuth_math_writing.rules.json",
        "rules/ieee_acm_citation.rules.json",
        "rules/theorem_proof_audit.rules.json",
    ]:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_bundle.py"),
                "--ruleset",
                str(ROOT / rel),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"{rel}\n{result.stdout}\n{result.stderr}"

def test_example_audit_report_parses() -> None:
    path = ROOT / "examples" / "sample_audit_report.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "verdict" in data
    assert "findings" in data
