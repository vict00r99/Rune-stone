"""
Tests for RUNE spec format compliance.

Validates that the RUNE specification format itself is consistent
by testing various well-formed and malformed specs against the
rules documented in SPEC.md.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest
import yaml

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FIELDS = {"meta", "RUNE", "SIGNATURE", "INTENT", "BEHAVIOR", "TESTS"}


def parse_spec(content: str) -> dict:
    """Parse a RUNE spec YAML string and return the dict."""
    return yaml.safe_load(content)


# ---------------------------------------------------------------------------
# Well-formed spec tests
# ---------------------------------------------------------------------------


class TestWellFormedSpecs:
    """Tests that well-formed specs parse correctly and contain expected fields."""

    def test_python_function_spec(self):
        spec_str = textwrap.dedent("""\
            ---
            meta:
              name: calculate_area
              language: python
              version: 1.0
              tags: [math, geometry]
            ---
            RUNE: calculate_area

            SIGNATURE: |
              def calculate_area(length: float, width: float) -> float

            INTENT: |
              Calculates the area of a rectangle given length and width.

            BEHAVIOR:
              - WHEN length <= 0 THEN raise ValueError("Length must be positive")
              - WHEN width <= 0 THEN raise ValueError("Width must be positive")
              - CALCULATE area = length * width
              - RETURN area

            CONSTRAINTS:
              - "length: positive float"
              - "width: positive float"

            EDGE_CASES:
              - "length = 0: raises ValueError"
              - "very large values: handles without overflow"

            TESTS:
              - "calculate_area(5.0, 3.0) == 15.0"
              - "calculate_area(1.0, 1.0) == 1.0"
              - "calculate_area(0, 3.0) raises ValueError"
              - "calculate_area(-1.0, 3.0) raises ValueError"

            COMPLEXITY:
              time: O(1)
              space: O(1)
        """)
        data = parse_spec(spec_str)
        assert set(REQUIRED_FIELDS).issubset(data.keys())
        assert data["meta"]["language"] == "python"
        assert data["RUNE"] == "calculate_area"
        assert len(data["TESTS"]) == 4

    def test_typescript_function_spec(self):
        spec_str = textwrap.dedent("""\
            ---
            meta:
              name: format_currency
              language: typescript
              version: 1.0
            ---
            RUNE: format_currency

            SIGNATURE: |
              function formatCurrency(amount: number, currency: string): string

            INTENT: |
              Formats a numeric amount as a currency string with proper symbol and decimals.

            BEHAVIOR:
              - WHEN amount is NaN THEN throw Error("Invalid amount")
              - WHEN currency is not recognized THEN throw Error("Unknown currency")
              - FORMAT amount with 2 decimal places
              - PREPEND currency symbol
              - RETURN formatted string

            TESTS:
              - "formatCurrency(10.5, 'USD') === '$10.50'"
              - "formatCurrency(1000, 'EUR') === '1,000.00'"
              - "formatCurrency(NaN, 'USD') throws Error"
        """)
        data = parse_spec(spec_str)
        assert data["meta"]["language"] == "typescript"
        assert "function formatCurrency" in data["SIGNATURE"]

    def test_async_python_spec(self):
        spec_str = textwrap.dedent("""\
            ---
            meta:
              name: fetch_user
              language: python
              version: 1.0
              tags: [async, api]
            ---
            RUNE: fetch_user

            SIGNATURE: |
              async def fetch_user(user_id: int) -> dict[str, Any]

            INTENT: |
              Fetches user data from the API by user ID.

            BEHAVIOR:
              - WHEN user_id < 1 THEN raise ValueError
              - PERFORM GET request to /users/{user_id}
              - RETURN parsed JSON response

            TESTS:
              - "await fetch_user(1) returns dict with 'name' key"
              - "await fetch_user(0) raises ValueError"
              - "await fetch_user(999999) raises NotFoundError"
        """)
        data = parse_spec(spec_str)
        assert "async def" in data["SIGNATURE"]
        assert len(data["TESTS"]) == 3


# ---------------------------------------------------------------------------
# Malformed spec tests
# ---------------------------------------------------------------------------


class TestMalformedSpecs:
    """Tests that malformed content is detected as YAML but missing fields."""

    def test_missing_meta(self):
        spec_str = textwrap.dedent("""\
            RUNE: test
            SIGNATURE: "def test() -> None"
            INTENT: "A test."
            BEHAVIOR:
              - WHEN called THEN pass
            TESTS:
              - "test() is None"
        """)
        data = parse_spec(spec_str)
        assert "meta" not in data

    def test_missing_tests(self):
        spec_str = textwrap.dedent("""\
            ---
            meta:
              name: test
              language: python
            ---
            RUNE: test
            SIGNATURE: "def test() -> None"
            INTENT: "A test."
            BEHAVIOR:
              - WHEN called THEN pass
        """)
        data = parse_spec(spec_str)
        assert "TESTS" not in data

    def test_empty_behavior(self):
        spec_str = textwrap.dedent("""\
            ---
            meta:
              name: test
              language: python
            ---
            RUNE: test
            SIGNATURE: "def test() -> None"
            INTENT: "A test."
            BEHAVIOR: []
            TESTS:
              - "test() is None"
        """)
        data = parse_spec(spec_str)
        assert data["BEHAVIOR"] == []

    def test_invalid_yaml(self):
        with pytest.raises(yaml.YAMLError):
            parse_spec("{ broken: [yaml")


# ---------------------------------------------------------------------------
# WHEN/THEN format tests
# ---------------------------------------------------------------------------


class TestBehaviorFormat:
    """Tests that BEHAVIOR entries follow WHEN/THEN conventions."""

    def test_when_then_format(self):
        behavior = [
            "WHEN input is empty THEN raise ValueError",
            "WHEN input is valid THEN process normally",
            "OTHERWISE return default",
        ]
        when_then_count = sum(1 for b in behavior if "WHEN" in b and "THEN" in b)
        assert when_then_count >= 2

    def test_otherwise_clause(self):
        behavior = [
            "WHEN x > 0 THEN return positive",
            "WHEN x < 0 THEN return negative",
            "OTHERWISE return zero",
        ]
        has_otherwise = any("OTHERWISE" in b for b in behavior)
        assert has_otherwise


# ---------------------------------------------------------------------------
# Cross-spec consistency tests
# ---------------------------------------------------------------------------


class TestCrossSpecConsistency:
    """Tests that existing .rune files in the repo are consistent."""

    def _load_all_specs(self) -> list[tuple[Path, dict]]:
        specs = []
        examples = REPO_ROOT / "examples"
        if examples.exists():
            for f in examples.rglob("*.rune"):
                if f.stat().st_size > 0:
                    try:
                        data = yaml.safe_load(f.read_text(encoding="utf-8"))
                        if isinstance(data, dict):
                            specs.append((f, data))
                    except yaml.YAMLError:
                        pass
        return specs

    def test_all_specs_have_consistent_naming(self):
        """meta.name should relate to RUNE field value."""
        for path, data in self._load_all_specs():
            meta_name = data.get("meta", {}).get("name", "")
            rune_name = str(data.get("RUNE", ""))
            # They don't have to be identical (meta.name can be a module name)
            # but both should be non-empty
            assert meta_name, f"{path.name}: meta.name is empty"
            assert rune_name, f"{path.name}: RUNE is empty"

    def test_all_specs_have_language(self):
        for path, data in self._load_all_specs():
            lang = data.get("meta", {}).get("language", "")
            assert lang, f"{path.name}: missing meta.language"

    def test_all_specs_have_at_least_one_test(self):
        for path, data in self._load_all_specs():
            tests = data.get("TESTS", [])
            assert isinstance(tests, list) and len(tests) >= 1, (
                f"{path.name}: TESTS must have at least one entry"
            )
