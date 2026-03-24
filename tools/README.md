# Tools

## validate_bundle.py

Validate either:

- a full bundle JSON file against `schemas/bundle.schema.json`, or
- a standalone ruleset JSON file against `schemas/rule_set.schema.json`

Examples:

```bash
python tools/validate_bundle.py --bundle bundles/math_paper_llm_auditor.bundle.json
python tools/validate_bundle.py --ruleset rules/knuth_math_writing.rules.json
```
