"""
RUNE Spec Parser

Parses .rune files into structured Python objects for programmatic access.
Validates structure and provides convenient attribute access to all spec fields.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

IDENTIFIER_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

REQUIRED_FIELDS = frozenset({"meta", "RUNE", "SIGNATURE", "INTENT", "BEHAVIOR", "TESTS"})
REQUIRED_META = frozenset({"name", "language"})

SUPPORTED_LANGUAGES = frozenset({
    "python", "typescript", "javascript", "go", "rust", "java",
    "csharp", "cpp", "c", "ruby", "php", "swift", "kotlin",
})


@dataclass
class RUNEComplexity:
    """Time and space complexity annotations."""
    time: str = ""
    space: str = ""


@dataclass
class RUNEMeta:
    """Metadata section of a RUNE spec."""
    name: str = ""
    language: str = ""
    version: str = "1.0"
    tags: list[str] = field(default_factory=list)
    agent: str = ""
    mcp_server: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class RUNESpec:
    """Parsed representation of a RUNE specification."""
    meta: RUNEMeta = field(default_factory=RUNEMeta)
    rune: str = ""
    signature: str = ""
    intent: str = ""
    behavior: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    edge_cases: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    complexity: RUNEComplexity = field(default_factory=RUNEComplexity)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.rune or self.meta.name

    @property
    def language(self) -> str:
        return self.meta.language

    @property
    def is_async(self) -> bool:
        return "async " in self.signature

    @property
    def has_tests(self) -> bool:
        return len(self.tests) > 0

    @property
    def test_count(self) -> int:
        return len(self.tests)

    def to_dict(self) -> dict[str, Any]:
        """Serialize back to a plain dict (for YAML output)."""
        result: dict[str, Any] = {
            "meta": {
                "name": self.meta.name,
                "language": self.meta.language,
                "version": self.meta.version,
            },
            "RUNE": self.rune,
            "SIGNATURE": self.signature,
            "INTENT": self.intent,
            "BEHAVIOR": self.behavior,
            "TESTS": self.tests,
        }
        if self.meta.tags:
            result["meta"]["tags"] = self.meta.tags
        if self.meta.agent:
            result["meta"]["agent"] = self.meta.agent
        if self.meta.mcp_server:
            result["meta"]["mcp_server"] = self.meta.mcp_server
        if self.constraints:
            result["CONSTRAINTS"] = self.constraints
        if self.edge_cases:
            result["EDGE_CASES"] = self.edge_cases
        if self.dependencies:
            result["DEPENDENCIES"] = self.dependencies
        if self.examples:
            result["EXAMPLES"] = self.examples
        if self.complexity.time or self.complexity.space:
            result["COMPLEXITY"] = {}
            if self.complexity.time:
                result["COMPLEXITY"]["time"] = self.complexity.time
            if self.complexity.space:
                result["COMPLEXITY"]["space"] = self.complexity.space
        return result


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


class ParseError(Exception):
    """Raised when a RUNE spec cannot be parsed."""


class ValidationError(Exception):
    """Raised when a RUNE spec fails structural validation."""


def _to_str_list(value: Any) -> list[str]:
    """Coerce a value to a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if item is not None]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return [str(value)]


class RUNEParser:
    """Parses RUNE spec YAML into RUNESpec objects."""

    def parse_string(self, content: str) -> RUNESpec:
        """Parse a RUNE spec from a YAML string."""
        if not content or not content.strip():
            raise ParseError("Spec content is empty")

        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as exc:
            raise ParseError(f"Invalid YAML: {exc}") from exc

        if not isinstance(data, dict):
            raise ParseError(f"Expected YAML mapping, got {type(data).__name__}")

        return self._build_spec(data)

    def parse_file(self, filepath: str | Path) -> RUNESpec:
        """Parse a RUNE spec from a file path."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Spec file not found: {filepath}")

        content = path.read_text(encoding="utf-8")
        spec = self.parse_string(content)
        return spec

    def validate(self, spec: RUNESpec) -> list[str]:
        """Validate a parsed RUNESpec. Returns list of error messages (empty = valid)."""
        errors: list[str] = []

        if not spec.meta.name:
            errors.append("meta.name is required")
        if not spec.meta.language:
            errors.append("meta.language is required")
        elif spec.meta.language not in SUPPORTED_LANGUAGES:
            errors.append(f"Unsupported language: {spec.meta.language}")
        if not spec.rune:
            errors.append("RUNE field is required")
        if not spec.signature.strip():
            errors.append("SIGNATURE is required")
        if not spec.intent.strip():
            errors.append("INTENT is required")
        if not spec.behavior:
            errors.append("BEHAVIOR must have at least one entry")
        if not spec.tests:
            errors.append("TESTS must have at least one entry")

        return errors

    def _build_spec(self, data: dict[str, Any]) -> RUNESpec:
        """Build a RUNESpec from parsed YAML data."""
        # Meta
        raw_meta = data.get("meta", {})
        if not isinstance(raw_meta, dict):
            raw_meta = {}

        meta = RUNEMeta(
            name=str(raw_meta.get("name", "")),
            language=str(raw_meta.get("language", "")),
            version=str(raw_meta.get("version", "1.0")),
            tags=_to_str_list(raw_meta.get("tags")),
            agent=str(raw_meta.get("agent", "")),
            mcp_server=str(raw_meta.get("mcp_server", "")),
            extra={k: v for k, v in raw_meta.items()
                   if k not in ("name", "language", "version", "tags", "agent", "mcp_server")},
        )

        # Complexity
        raw_complexity = data.get("COMPLEXITY", {})
        if not isinstance(raw_complexity, dict):
            raw_complexity = {}
        complexity = RUNEComplexity(
            time=str(raw_complexity.get("time", "")),
            space=str(raw_complexity.get("space", "")),
        )

        return RUNESpec(
            meta=meta,
            rune=str(data.get("RUNE", "")),
            signature=str(data.get("SIGNATURE", "")).strip(),
            intent=str(data.get("INTENT", "")).strip(),
            behavior=_to_str_list(data.get("BEHAVIOR")),
            tests=_to_str_list(data.get("TESTS")),
            constraints=_to_str_list(data.get("CONSTRAINTS")),
            edge_cases=_to_str_list(data.get("EDGE_CASES")),
            dependencies=_to_str_list(data.get("DEPENDENCIES")),
            examples=_to_str_list(data.get("EXAMPLES")),
            complexity=complexity,
            raw=data,
        )


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------

_default_parser = RUNEParser()


def parse_rune_string(content: str) -> RUNESpec:
    """Parse a RUNE spec from a YAML string."""
    return _default_parser.parse_string(content)


def parse_rune_file(filepath: str | Path) -> RUNESpec:
    """Parse a RUNE spec from a file path."""
    return _default_parser.parse_file(filepath)
