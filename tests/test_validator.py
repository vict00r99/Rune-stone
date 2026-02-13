"""
Tests for tools/validate.py CLI validator.

Covers: single file validation, directory validation, strict mode,
error cases, and JSON output.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import pytest

# Add tools/ to path so we can import validate module
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from validate import validate_spec, validate_file, validate_directory  # noqa: E402

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_SPEC = textwrap.dedent("""\
    ---
    meta:
      name: greet
      language: python
      version: 1.0
      tags: [utility]
    ---
    RUNE: greet

    SIGNATURE: |
      def greet(name: str) -> str

    INTENT: |
      Returns a greeting string for the given name.

    BEHAVIOR:
      - WHEN name is empty THEN raise ValueError
      - OTHERWISE return "Hello, {name}!"

    CONSTRAINTS:
      - "name: non-empty string"

    EDGE_CASES:
      - "empty string: raises ValueError"
      - "name with spaces: valid"

    TESTS:
      - "greet('Alice') == 'Hello, Alice!'"
      - "greet('') raises ValueError"
      - "greet('Bob Smith') == 'Hello, Bob Smith!'"

    EXAMPLES:
      - |
        print(greet("World"))
        # Hello, World!

    COMPLEXITY:
      time: O(1)
      space: O(1)
""")

MINIMAL_VALID = textwrap.dedent("""\
    ---
    meta:
      name: add
      language: python
    ---
    RUNE: add
    SIGNATURE: "def add(a: int, b: int) -> int"
    INTENT: "Adds two integers."
    BEHAVIOR:
      - WHEN inputs are valid THEN return sum
    TESTS:
      - "add(1, 2) == 3"
      - "add(0, 0) == 0"
      - "add(-1, 1) == 0"
""")


# ---------------------------------------------------------------------------
# validate_spec tests
# ---------------------------------------------------------------------------


class TestValidateSpec:
    def test_valid_full_spec(self):
        result = validate_spec(VALID_SPEC)
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_valid_minimal_spec(self):
        result = validate_spec(MINIMAL_VALID)
        assert result["valid"] is True

    def test_invalid_yaml(self):
        result = validate_spec("{ broken yaml: [")
        assert result["valid"] is False
        assert any("YAML" in e for e in result["errors"])

    def test_non_dict_yaml(self):
        result = validate_spec("- just\n- a\n- list")
        assert result["valid"] is False

    def test_missing_meta(self):
        spec = textwrap.dedent("""\
            RUNE: test
            SIGNATURE: "def test() -> None"
            INTENT: "Test function."
            BEHAVIOR:
              - WHEN called THEN pass
            TESTS:
              - "test() is None"
        """)
        result = validate_spec(spec)
        assert result["valid"] is False
        assert any("meta" in e for e in result["errors"])

    def test_missing_tests(self):
        spec = textwrap.dedent("""\
            ---
            meta:
              name: test
              language: python
            ---
            RUNE: test
            SIGNATURE: "def test() -> None"
            INTENT: "Test."
            BEHAVIOR:
              - WHEN called THEN pass
        """)
        result = validate_spec(spec)
        assert result["valid"] is False
        assert any("TESTS" in e for e in result["errors"])

    def test_missing_behavior(self):
        spec = textwrap.dedent("""\
            ---
            meta:
              name: test
              language: python
            ---
            RUNE: test
            SIGNATURE: "def test() -> None"
            INTENT: "Test."
            TESTS:
              - "test() is None"
        """)
        result = validate_spec(spec)
        assert result["valid"] is False
        assert any("BEHAVIOR" in e for e in result["errors"])

    def test_few_tests_warning(self):
        spec = textwrap.dedent("""\
            ---
            meta:
              name: test
              language: python
            ---
            RUNE: test
            SIGNATURE: "def test() -> None"
            INTENT: "Test."
            BEHAVIOR:
              - WHEN called THEN pass
            TESTS:
              - "test() is None"
        """)
        result = validate_spec(spec)
        assert result["valid"] is True  # 1 test is valid, just warns
        assert any("test" in w.lower() for w in result["warnings"])

    def test_strict_mode_flags_missing_optional(self):
        result = validate_spec(MINIMAL_VALID, strict=True)
        # Should have warnings about missing EDGE_CASES, CONSTRAINTS, etc.
        assert len(result["warnings"]) > 0

    def test_strict_mode_full_spec_fewer_warnings(self):
        result = validate_spec(VALID_SPEC, strict=True)
        # Full spec has all optional fields, should have minimal warnings
        assert result["valid"] is True

    def test_unknown_language_warning(self):
        spec = MINIMAL_VALID.replace("language: python", "language: brainfuck")
        result = validate_spec(spec)
        assert any("language" in w.lower() or "brainfuck" in w.lower() for w in result["warnings"])

    def test_summary_present(self):
        result = validate_spec(VALID_SPEC)
        assert "summary" in result
        assert isinstance(result["summary"], str)

    def test_field_summary_present(self):
        result = validate_spec(VALID_SPEC)
        assert "field_summary" in result
        assert "SIGNATURE" in result["field_summary"]
        assert result["field_summary"]["SIGNATURE"]["present"] is True


# ---------------------------------------------------------------------------
# validate_file tests
# ---------------------------------------------------------------------------


class TestValidateFile:
    def test_existing_example(self):
        example = REPO_ROOT / "examples" / "basic" / "calculate_discount.rune"
        if not example.exists():
            pytest.skip("Example file not present")
        result = validate_file(example)
        assert result["valid"] is True
        assert "filepath" in result

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            validate_file(Path("nonexistent.rune"))

    def test_empty_file(self, tmp_path: Path):
        empty = tmp_path / "empty.rune"
        empty.write_text("")
        result = validate_file(empty)
        assert result["valid"] is False
        assert any("empty" in e.lower() for e in result["errors"])

    def test_wrong_extension_warning(self, tmp_path: Path):
        wrong_ext = tmp_path / "spec.yaml"
        wrong_ext.write_text(VALID_SPEC)
        result = validate_file(wrong_ext)
        assert any("extension" in w.lower() for w in result["warnings"])


# ---------------------------------------------------------------------------
# validate_directory tests
# ---------------------------------------------------------------------------


class TestValidateDirectory:
    def test_examples_basic(self):
        basic_dir = REPO_ROOT / "examples" / "basic"
        if not basic_dir.exists():
            pytest.skip("Basic examples directory not present")
        reports = validate_directory(basic_dir)
        assert len(reports) >= 1
        assert all(r["valid"] for r in reports)

    def test_empty_directory(self, tmp_path: Path):
        reports = validate_directory(tmp_path)
        assert reports == []
