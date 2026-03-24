# Mathematics Paper LLM Auditor

A CI-ready repository bundle for LLM-assisted auditing of mathematical papers.

It packages three rulesets:

1. **Knuth-style mathematical writing** checks
2. **IEEE / ACM citation** checks
3. **Theorem-and-proof rigor** checks

The bundle is designed to validate cleanly with JSON Schema and to be easy to use from CI, scripts, or an LLM prompt pipeline. It is based on the repository structure and rule content provided in the source material. See the original source text included by the user for the design rationale and provenance. This repo was generated from that material.

## Repository layout

```text
math_paper_llm_auditor/
├── .github/workflows/ci.yml
├── LICENSE
├── NOTICE.md
├── README.md
├── bundles/math_paper_llm_auditor.bundle.json
├── examples/
├── manifest.json
├── requirements.txt
├── rules/
├── schemas/
├── scripts/package_zip.sh
├── tests/test_repo.py
└── tools/
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python tools/validate_bundle.py --bundle bundles/math_paper_llm_auditor.bundle.json
python tools/validate_bundle.py --ruleset rules/knuth_math_writing.rules.json
python tools/validate_bundle.py --ruleset rules/ieee_acm_citation.rules.json
python tools/validate_bundle.py --ruleset rules/theorem_proof_audit.rules.json
pytest -q
```

## What is included

- `bundles/math_paper_llm_auditor.bundle.json`: combined entry-point bundle
- `rules/*.rules.json`: standalone rulesets
- `schemas/*.schema.json`: JSON Schemas for rulesets, bundles, and audit reports
- `examples/sample_audit_report.json`: example schema-valid report
- `examples/sample_target_metadata.json`: minimal metadata example for a target document
- `tools/validate_bundle.py`: schema validator for a bundle or standalone ruleset
- `.github/workflows/ci.yml`: minimal CI validation workflow

## Expected audit workflow

1. Normalize the target paper text into LaTeX, Markdown, or plaintext.
2. Select the relevant venue profile and rulesets.
3. Run deterministic checks.
4. Run LLM semantic audit with quoted evidence.
5. Emit an audit report using `schemas/audit_report.schema.json`.

## Notes

- The rules summarize public style guidance; they do not redistribute the publisher standards themselves.
- The citation ruleset contains both IEEE and ACM profiles in one ruleset.
- The theorem/proof ruleset is deliberately strict and intended for reviewer-style auditing.
