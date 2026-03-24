#!/usr/bin/env python3
"""
Validate the JSON bundle files with jsonschema and perform a few structural checks:
- file exists
- JSON parses
- schema validates (bundle / ruleset)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main(bundle_path: str) -> int:
    try:
        import jsonschema  # type: ignore
    except Exception:
        print("Missing dependency: jsonschema. Install with `pip install jsonschema`.")
        return 2

    bundle_path_obj = Path(bundle_path)
    if not bundle_path_obj.exists():
        print(f"[FAIL] Bundle not found: {bundle_path_obj}")
        return 1

    data = load_json(bundle_path_obj)

    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "bundle.schema.json"
    schema = load_json(schema_path)

    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        print(f"[FAIL] Bundle schema validation failed: {bundle_path_obj}")
        print(e)
        return 1

    # Lightweight checks: referenced files exist
    repo_root = bundle_path_obj.parent.parent
    for rs in data.get("rulesets", []):
        rel = rs.get("path")
        if rel:
            p = repo_root / rel
            if not p.exists():
                print(f"[FAIL] Missing referenced ruleset file: {p}")
                return 1

    for sp in data.get("schemas", []):
        p = repo_root / sp
        if not p.exists():
            print(f"[FAIL] Missing referenced schema file: {p}")
            return 1

    print(f"[OK] Bundle validated: {bundle_path_obj}")
    return 0


# ---- Added in CI-ready fork: support validating standalone rulesets ----

def _validate_ruleset_file(path: str) -> int:
    try:
        import jsonschema  # type: ignore
    except Exception:
        print("Missing dependency: jsonschema. Install with `pip install jsonschema`.")
        return 2

    ruleset_path = Path(path)
    data = load_json(ruleset_path)
    schema_path = Path(__file__).resolve().parent.parent / "schemas" / "rule_set.schema.json"
    schema = load_json(schema_path)
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        print(f"[FAIL] Ruleset schema validation failed: {ruleset_path}")
        print(e)
        return 1
    print(f"[OK] Ruleset schema validated: {ruleset_path}")
    return 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate bundle and/or standalone ruleset JSON files.")
    parser.add_argument("--bundle", type=str, default=None, help="Path to a bundle JSON file to validate.")
    parser.add_argument("--ruleset", type=str, default=None, help="Path to a ruleset JSON file to validate.")
    args = parser.parse_args()

    if args.bundle:
        raise SystemExit(main(args.bundle))
    if args.ruleset:
        raise SystemExit(_validate_ruleset_file(args.ruleset))

    parser.error("Must supply --bundle or --ruleset")
