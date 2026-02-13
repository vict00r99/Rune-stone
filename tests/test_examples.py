"""
Tests that validate all example .rune files in the repository.

Ensures every example is valid YAML, has all required fields,
follows RUNE conventions, and meets minimum quality standards.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
TOOLS_DIR = REPO_ROOT / "tools"

REQUIRED_FIELDS = {"meta", "RUNE", "SIGNATURE", "INTENT", "BEHAVIOR", "TESTS"}
REQUIRED_META = {"name", "language"}
SUPPORTED_LANGUAGES = {
    "python", "typescript", "javascript", "go", "rust", "java",
    "csharp", "cpp", "c", "ruby", "php", "swift", "kotlin",
}


def discover_rune_files(*dirs: Path) -> list[Path]:
    """Find all non-empty .rune files under the given directories."""
    files = []
    for d in dirs:
        if d.exists():
            for f in sorted(d.rglob("*.rune")):
                if f.stat().st_size > 0:
                    files.append(f)
    return files


RUNE_FILES = discover_rune_files(EXAMPLES_DIR, TOOLS_DIR)

# Skip the templates directory -- those are intentionally placeholder-style
TEMPLATE_DIR = REPO_ROOT / "templates"


# ---------------------------------------------------------------------------
# Parametrized tests over all .rune files
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "rune_path",
    RUNE_FILES,
    ids=[str(p.relative_to(REPO_ROOT)) for p in RUNE_FILES],
)
class TestRuneExamples:
    """Validates every .rune example and tool spec."""

    def test_valid_yaml(self, rune_path: Path):
        """File must be parseable as YAML."""
        content = rune_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        assert isinstance(data, dict), f"Expected YAML dict, got {type(data).__name__}"

    def test_required_fields_present(self, rune_path: Path):
        """All required RUNE fields must exist."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        missing = REQUIRED_FIELDS - set(data.keys())
        assert not missing, f"Missing required fields: {missing}"

    def test_meta_section(self, rune_path: Path):
        """meta must contain name and language."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        meta = data.get("meta", {})
        assert isinstance(meta, dict), "meta must be a dict"
        missing_meta = REQUIRED_META - set(meta.keys())
        assert not missing_meta, f"Missing meta fields: {missing_meta}"

    def test_meta_language_supported(self, rune_path: Path):
        """meta.language must be a recognized language."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        lang = data.get("meta", {}).get("language", "")
        assert lang in SUPPORTED_LANGUAGES, f"Unsupported language: {lang}"

    def test_signature_non_empty(self, rune_path: Path):
        """SIGNATURE must be a non-empty string."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        sig = data.get("SIGNATURE", "")
        assert isinstance(sig, str) and sig.strip(), "SIGNATURE must be non-empty"

    def test_intent_non_empty(self, rune_path: Path):
        """INTENT must be a non-empty string."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        intent = data.get("INTENT", "")
        assert isinstance(intent, str) and intent.strip(), "INTENT must be non-empty"

    def test_behavior_is_list(self, rune_path: Path):
        """BEHAVIOR must be a non-empty list."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        behavior = data.get("BEHAVIOR", [])
        assert isinstance(behavior, list), "BEHAVIOR must be a list"
        assert len(behavior) >= 1, "BEHAVIOR must have at least one entry"

    def test_tests_is_list_with_entries(self, rune_path: Path):
        """TESTS must be a list with at least one entry."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        tests = data.get("TESTS", [])
        assert isinstance(tests, list), "TESTS must be a list"
        assert len(tests) >= 1, "TESTS must have at least one entry"

    def test_minimum_three_tests(self, rune_path: Path):
        """Best practice: at least 3 test cases."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        tests = data.get("TESTS", [])
        # This is a quality check, not a hard requirement
        if len(tests) < 3:
            pytest.xfail(f"Only {len(tests)} test(s); 3+ recommended")

    def test_rune_field_is_identifier(self, rune_path: Path):
        """RUNE field must be a valid identifier."""
        data = yaml.safe_load(rune_path.read_text(encoding="utf-8"))
        rune_name = str(data.get("RUNE", ""))
        assert rune_name, "RUNE field must be non-empty"
        assert rune_name.replace("_", "").replace("-", "").isalnum(), (
            f"RUNE value '{rune_name}' should be a valid identifier"
        )

    def test_file_extension(self, rune_path: Path):
        """File should have .rune extension."""
        assert rune_path.suffix == ".rune"


# ---------------------------------------------------------------------------
# Template validation (separate, lighter checks)
# ---------------------------------------------------------------------------


def discover_template_files() -> list[Path]:
    if TEMPLATE_DIR.exists():
        return [f for f in sorted(TEMPLATE_DIR.glob("*.rune")) if f.stat().st_size > 0]
    return []


TEMPLATE_FILES = discover_template_files()


@pytest.mark.parametrize(
    "template_path",
    TEMPLATE_FILES,
    ids=[p.name for p in TEMPLATE_FILES],
)
class TestTemplates:
    """Light validation for template files (they contain placeholders)."""

    def test_valid_yaml_syntax(self, template_path: Path):
        """Template must be parseable as YAML (placeholders are strings)."""
        content = template_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        assert isinstance(data, dict), "Template must be a YAML dict"

    def test_has_rune_structure(self, template_path: Path):
        """Template must contain the core RUNE field names."""
        data = yaml.safe_load(template_path.read_text(encoding="utf-8"))
        expected = {"meta", "RUNE", "SIGNATURE", "INTENT", "BEHAVIOR", "TESTS"}
        present = set(data.keys()) & expected
        assert len(present) >= 5, f"Template missing core fields: {expected - present}"
