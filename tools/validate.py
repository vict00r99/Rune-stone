"""
RUNE Spec Validator

Validates .rune files against the RUNE specification standard (SPEC.md).
Checks structural correctness, required fields, content quality, and best practices.

Usage:
    python tools/validate.py <path>              # validate file or directory
    python tools/validate.py --strict <path>     # strict mode (check optional fields)
    python tools/validate.py --json <path>       # output results as JSON
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {"meta", "RUNE", "SIGNATURE", "INTENT", "BEHAVIOR", "TESTS"}
REQUIRED_META_FIELDS = {"name", "language"}
OPTIONAL_FIELDS = {"CONSTRAINTS", "EDGE_CASES", "DEPENDENCIES", "EXAMPLES", "COMPLEXITY"}
SUPPORTED_LANGUAGES = {
    "python", "typescript", "javascript", "go", "rust", "java",
    "csharp", "cpp", "c", "ruby", "php", "swift", "kotlin",
}
LIST_FIELDS = {"BEHAVIOR", "TESTS", "CONSTRAINTS", "EDGE_CASES", "DEPENDENCIES", "EXAMPLES"}
IDENTIFIER_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------


def validate_spec(content: str, *, strict: bool = False) -> dict[str, Any]:
    """Validate a RUNE spec string and return a report."""
    errors: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []
    field_summary: dict[str, Any] = {}

    # --- Parse YAML ---
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return {
            "valid": False,
            "errors": [f"Invalid YAML: {exc}"],
            "warnings": [],
            "suggestions": ["Fix the YAML syntax errors and re-validate"],
            "field_summary": {},
        }

    if not isinstance(data, dict):
        return {
            "valid": False,
            "errors": ["Spec must be a YAML mapping (dict), got " + type(data).__name__],
            "warnings": [],
            "suggestions": ["Ensure the file starts with --- and contains key: value pairs"],
            "field_summary": {},
        }

    # --- Required fields ---
    for field in REQUIRED_FIELDS:
        if field in data:
            field_summary[field] = {"present": True}
            if field in LIST_FIELDS and isinstance(data[field], list):
                field_summary[field]["count"] = len(data[field])
        else:
            errors.append(f"Missing required field: {field}")
            field_summary[field] = {"present": False}

    # --- meta section ---
    meta = data.get("meta")
    if isinstance(meta, dict):
        for mf in REQUIRED_META_FIELDS:
            if mf not in meta:
                errors.append(f"Missing required meta field: meta.{mf}")
        lang = meta.get("language", "")
        if lang and lang not in SUPPORTED_LANGUAGES:
            warnings.append(f"Unrecognized language '{lang}' (supported: {', '.join(sorted(SUPPORTED_LANGUAGES))})")
        name = meta.get("name", "")
        if name and not IDENTIFIER_RE.match(name):
            warnings.append(f"meta.name '{name}' is not a valid identifier")
    elif meta is not None:
        errors.append("meta must be a mapping (dict)")

    # --- RUNE field ---
    rune_name = data.get("RUNE", "")
    if rune_name and not IDENTIFIER_RE.match(str(rune_name)):
        warnings.append(f"RUNE value '{rune_name}' is not a valid identifier")

    # --- SIGNATURE ---
    sig = data.get("SIGNATURE", "")
    if isinstance(sig, str) and sig.strip():
        # Basic check: should contain function/class keyword or type annotation
        sig_lower = sig.strip().lower()
        has_keyword = any(kw in sig_lower for kw in ["def ", "func ", "function ", "class ", "fn ", "pub ", "async "])
        if not has_keyword:
            warnings.append("SIGNATURE may not use target language syntax (no function/class keyword found)")
    elif "SIGNATURE" in data:
        errors.append("SIGNATURE must be a non-empty string")

    # --- INTENT ---
    intent = data.get("INTENT", "")
    if isinstance(intent, str) and intent.strip():
        sentences = [s.strip() for s in intent.strip().split(".") if s.strip()]
        if len(sentences) > 5:
            warnings.append(f"INTENT has {len(sentences)} sentences (recommended: 1-3)")
    elif "INTENT" in data:
        errors.append("INTENT must be a non-empty string")

    # --- BEHAVIOR ---
    behavior = data.get("BEHAVIOR", [])
    if isinstance(behavior, list):
        if len(behavior) == 0:
            errors.append("BEHAVIOR must have at least one entry")
        has_when_then = any("WHEN" in str(b) and "THEN" in str(b) for b in behavior)
        if not has_when_then and len(behavior) > 0:
            suggestions.append("Consider using WHEN/THEN format in BEHAVIOR for clarity")
    elif "BEHAVIOR" in data:
        errors.append("BEHAVIOR must be a list")

    # --- TESTS ---
    tests = data.get("TESTS", [])
    if isinstance(tests, list):
        if len(tests) == 0:
            errors.append("TESTS must have at least one test case")
        elif len(tests) < 3:
            warnings.append(f"TESTS has {len(tests)} cases (recommended minimum: 3)")
            suggestions.append("Add test cases for: happy path, boundary conditions, and error cases")
    elif "TESTS" in data:
        errors.append("TESTS must be a list")

    # --- Optional fields (strict mode) ---
    for field in OPTIONAL_FIELDS:
        if field in data:
            field_summary[field] = {"present": True}
            if field in LIST_FIELDS and isinstance(data[field], list):
                field_summary[field]["count"] = len(data[field])
            elif field == "COMPLEXITY" and isinstance(data[field], dict):
                field_summary[field]["keys"] = list(data[field].keys())
        else:
            field_summary[field] = {"present": False}
            if strict:
                warnings.append(f"Missing optional field: {field} (required in strict mode)")

    if strict:
        edge_cases = data.get("EDGE_CASES", [])
        if isinstance(edge_cases, list) and len(edge_cases) < 2:
            warnings.append(f"EDGE_CASES has {len(edge_cases)} entries (strict minimum: 2)")

        examples = data.get("EXAMPLES", [])
        if isinstance(examples, list) and len(examples) < 1:
            warnings.append("EXAMPLES should have at least 1 entry in strict mode")

    # --- Summary ---
    valid = len(errors) == 0
    summary_parts = []
    if valid:
        summary_parts.append("Valid RUNE specification")
    else:
        summary_parts.append(f"Invalid: {len(errors)} error(s)")
    if warnings:
        summary_parts.append(f"{len(warnings)} warning(s)")
    summary = ". ".join(summary_parts)

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions,
        "field_summary": field_summary,
        "summary": summary,
    }


def validate_file(filepath: Path, *, strict: bool = False) -> dict[str, Any]:
    """Validate a single .rune file."""
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    content = filepath.read_text(encoding="utf-8")
    if not content.strip():
        return {
            "valid": False,
            "filepath": str(filepath),
            "errors": ["File is empty"],
            "warnings": [],
            "suggestions": ["Add RUNE spec content to the file"],
            "field_summary": {},
        }

    report = validate_spec(content, strict=strict)
    report["filepath"] = str(filepath)

    if filepath.suffix != ".rune":
        report["warnings"].append(f"File extension is '{filepath.suffix}', expected '.rune'")

    return report


def validate_directory(dirpath: Path, *, strict: bool = False) -> list[dict[str, Any]]:
    """Validate all .rune files in a directory (recursively)."""
    reports = []
    for rune_file in sorted(dirpath.rglob("*.rune")):
        reports.append(validate_file(rune_file, strict=strict))
    return reports


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate RUNE specification files",
        epilog="Examples:\n"
               "  python tools/validate.py examples/basic/calculate_discount.rune\n"
               "  python tools/validate.py --strict examples/\n"
               "  python tools/validate.py --json examples/basic/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", help="Path to a .rune file or directory")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    args = parser.parse_args()

    target = Path(args.path)

    if target.is_file():
        reports = [validate_file(target, strict=args.strict)]
    elif target.is_dir():
        reports = validate_directory(target, strict=args.strict)
        if not reports:
            print(f"No .rune files found in {target}")
            return 1
    else:
        print(f"Path not found: {target}")
        return 1

    if args.json_output:
        print(json.dumps(reports, indent=2))
    else:
        total = len(reports)
        passed = sum(1 for r in reports if r["valid"])
        failed = total - passed

        for report in reports:
            filepath = report.get("filepath", "unknown")
            if report["valid"]:
                print(f"  PASS  {filepath}")
            else:
                print(f"  FAIL  {filepath}")
                for err in report["errors"]:
                    print(f"        ERROR: {err}")

            for warn in report.get("warnings", []):
                print(f"        WARN:  {warn}")
            for sug in report.get("suggestions", []):
                print(f"        FIX:   {sug}")

        print()
        print(f"Results: {passed} passed, {failed} failed, {total} total")

    return 0 if all(r["valid"] for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
