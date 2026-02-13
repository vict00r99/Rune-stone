"""
Tests for the RUNE spec parser (mcp-server/parser.py).

Covers: parsing from strings, parsing from files, validation,
edge cases, and data access on RUNESpec objects.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

# Adjust import path -- parser lives in mcp-server/ (hyphenated directory)
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mcp-server"))

from parser import (  # noqa: E402
    RUNEParser,
    RUNESpec,
    ParseError,
    parse_rune_string,
    parse_rune_file,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MINIMAL_SPEC = textwrap.dedent("""\
    ---
    meta:
      name: add
      language: python
      version: 1.0
    ---
    RUNE: add

    SIGNATURE: |
      def add(a: int, b: int) -> int

    INTENT: |
      Adds two integers and returns the sum.

    BEHAVIOR:
      - WHEN inputs are valid THEN return a + b

    TESTS:
      - "add(1, 2) == 3"
      - "add(0, 0) == 0"
      - "add(-1, 1) == 0"
""")

FULL_SPEC = textwrap.dedent("""\
    ---
    meta:
      name: calculate_discount
      language: python
      version: 1.0
      tags: [business-logic, calculation]
      agent: pricing_agent
    ---
    RUNE: calculate_discount

    SIGNATURE: |
      def calculate_discount(price: float, percentage: int) -> float

    INTENT: |
      Calculates the final price after applying a discount percentage.

    BEHAVIOR:
      - WHEN percentage < 0 THEN raise ValueError
      - WHEN percentage > 100 THEN raise ValueError
      - WHEN price < 0 THEN raise ValueError
      - CALCULATE final_price = price * (1 - percentage / 100)
      - RETURN final_price rounded to 2 decimals

    CONSTRAINTS:
      - "price: must be non-negative float"
      - "percentage: must be integer between 0 and 100"

    EDGE_CASES:
      - "percentage = 0: returns original price"
      - "percentage = 100: returns 0.0"

    TESTS:
      - "calculate_discount(100.0, 20) == 80.0"
      - "calculate_discount(50.0, 10) == 45.0"
      - "calculate_discount(0.0, 20) == 0.0"
      - "calculate_discount(-10.0, 20) raises ValueError"

    DEPENDENCIES:
      - "math (standard library)"

    EXAMPLES:
      - |
        result = calculate_discount(100.0, 20)
        # Returns: 80.0

    COMPLEXITY:
      time: O(1)
      space: O(1)
""")

ASYNC_SPEC = textwrap.dedent("""\
    ---
    meta:
      name: fetch_data
      language: python
      version: 1.0
      tags: [async, http]
    ---
    RUNE: fetch_data

    SIGNATURE: |
      async def fetch_data(url: str) -> dict

    INTENT: |
      Fetches JSON data from a URL asynchronously.

    BEHAVIOR:
      - WHEN url is empty THEN raise ValueError
      - PERFORM GET request to url
      - RETURN parsed JSON response

    TESTS:
      - "await fetch_data('https://example.com/api') returns dict"
      - "await fetch_data('') raises ValueError"
      - "await fetch_data('invalid') raises ConnectionError"
""")


@pytest.fixture
def parser():
    return RUNEParser()


# ---------------------------------------------------------------------------
# Parsing from strings
# ---------------------------------------------------------------------------


class TestParseString:
    def test_minimal_spec(self, parser: RUNEParser):
        spec = parser.parse_string(MINIMAL_SPEC)
        assert spec.name == "add"
        assert spec.language == "python"
        assert spec.rune == "add"
        assert "def add" in spec.signature
        assert "Adds two integers" in spec.intent
        assert len(spec.behavior) == 1
        assert len(spec.tests) == 3

    def test_full_spec(self, parser: RUNEParser):
        spec = parser.parse_string(FULL_SPEC)
        assert spec.name == "calculate_discount"
        assert spec.meta.tags == ["business-logic", "calculation"]
        assert spec.meta.agent == "pricing_agent"
        assert len(spec.constraints) == 2
        assert len(spec.edge_cases) == 2
        assert len(spec.tests) == 4
        assert len(spec.dependencies) == 1
        assert len(spec.examples) == 1
        assert spec.complexity.time == "O(1)"
        assert spec.complexity.space == "O(1)"

    def test_async_spec(self, parser: RUNEParser):
        spec = parser.parse_string(ASYNC_SPEC)
        assert spec.is_async is True
        assert spec.name == "fetch_data"

    def test_sync_spec_not_async(self, parser: RUNEParser):
        spec = parser.parse_string(MINIMAL_SPEC)
        assert spec.is_async is False

    def test_empty_string_raises(self, parser: RUNEParser):
        with pytest.raises(ParseError):
            parser.parse_string("")

    def test_whitespace_only_raises(self, parser: RUNEParser):
        with pytest.raises(ParseError):
            parser.parse_string("   \n\n  ")

    def test_invalid_yaml_raises(self, parser: RUNEParser):
        with pytest.raises(ParseError, match="Invalid YAML"):
            parser.parse_string("{ invalid yaml: [")

    def test_non_dict_yaml_raises(self, parser: RUNEParser):
        with pytest.raises(ParseError, match="mapping"):
            parser.parse_string("- just\n- a\n- list\n")


# ---------------------------------------------------------------------------
# Parsing from files
# ---------------------------------------------------------------------------


class TestParseFile:
    def test_parse_existing_example(self):
        example_path = Path(__file__).resolve().parent.parent / "examples" / "basic" / "calculate_discount.rune"
        if not example_path.exists():
            pytest.skip("Example file not found")
        spec = parse_rune_file(example_path)
        assert spec.name == "calculate_discount"
        assert spec.language == "python"
        assert spec.has_tests

    def test_file_not_found(self, parser: RUNEParser):
        with pytest.raises(FileNotFoundError):
            parser.parse_file("nonexistent_file.rune")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_valid_minimal_spec(self, parser: RUNEParser):
        spec = parser.parse_string(MINIMAL_SPEC)
        errors = parser.validate(spec)
        assert errors == []

    def test_valid_full_spec(self, parser: RUNEParser):
        spec = parser.parse_string(FULL_SPEC)
        errors = parser.validate(spec)
        assert errors == []

    def test_missing_meta_name(self, parser: RUNEParser):
        bad_spec = MINIMAL_SPEC.replace("name: add", "# name removed")
        spec = parser.parse_string(bad_spec)
        errors = parser.validate(spec)
        assert any("meta.name" in e for e in errors)

    def test_missing_meta_language(self, parser: RUNEParser):
        bad_spec = MINIMAL_SPEC.replace("language: python", "# language removed")
        spec = parser.parse_string(bad_spec)
        errors = parser.validate(spec)
        assert any("meta.language" in e for e in errors)

    def test_empty_tests(self, parser: RUNEParser):
        bad_spec = MINIMAL_SPEC.replace(
            'TESTS:\n  - "add(1, 2) == 3"\n  - "add(0, 0) == 0"\n  - "add(-1, 1) == 0"',
            "TESTS: []",
        )
        spec = parser.parse_string(bad_spec)
        errors = parser.validate(spec)
        assert any("TESTS" in e for e in errors)

    def test_empty_behavior(self, parser: RUNEParser):
        bad_spec = MINIMAL_SPEC.replace(
            "BEHAVIOR:\n  - WHEN inputs are valid THEN return a + b",
            "BEHAVIOR: []",
        )
        spec = parser.parse_string(bad_spec)
        errors = parser.validate(spec)
        assert any("BEHAVIOR" in e for e in errors)


# ---------------------------------------------------------------------------
# RUNESpec properties and methods
# ---------------------------------------------------------------------------


class TestRUNESpecProperties:
    def test_name_from_rune(self, parser: RUNEParser):
        spec = parser.parse_string(MINIMAL_SPEC)
        assert spec.name == "add"

    def test_test_count(self, parser: RUNEParser):
        spec = parser.parse_string(MINIMAL_SPEC)
        assert spec.test_count == 3

    def test_has_tests(self, parser: RUNEParser):
        spec = parser.parse_string(MINIMAL_SPEC)
        assert spec.has_tests is True

    def test_to_dict_roundtrip(self, parser: RUNEParser):
        spec = parser.parse_string(FULL_SPEC)
        d = spec.to_dict()
        assert d["RUNE"] == "calculate_discount"
        assert d["meta"]["language"] == "python"
        assert len(d["TESTS"]) == 4
        assert d["COMPLEXITY"]["time"] == "O(1)"


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------


class TestConvenienceFunctions:
    def test_parse_rune_string(self):
        spec = parse_rune_string(MINIMAL_SPEC)
        assert spec.name == "add"

    def test_parse_rune_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_rune_file("does_not_exist.rune")
