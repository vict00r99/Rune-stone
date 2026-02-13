"""
Runestone MCP Server

Exposes RUNE spec parsing and validation as MCP tools so AI assistants
can read, validate, and summarize .rune specification files.

Tools:
  - parse_rune_spec: Parse a .rune file and return structured data
  - validate_rune_spec: Validate a .rune file against SPEC.md standards
  - list_rune_specs: List all .rune files in a directory

Usage:
    python -m mcp_server
    # or
    python mcp-server/server.py
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server.lowlevel import Server
import mcp.server.stdio
from mcp.types import TextContent, Tool

from .parser import RUNEParser, ParseError

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

server = Server("runestone")
_parser = RUNEParser()

# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


async def _parse_rune_spec(filepath: str) -> dict[str, Any]:
    """Parse a .rune file and return its structured contents."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if not path.suffix == ".rune":
        raise ValueError(f"Expected .rune file, got: {path.suffix}")

    spec = _parser.parse_file(path)
    return {
        "name": spec.name,
        "language": spec.language,
        "signature": spec.signature,
        "intent": spec.intent,
        "behavior": spec.behavior,
        "tests": spec.tests,
        "constraints": spec.constraints,
        "edge_cases": spec.edge_cases,
        "dependencies": spec.dependencies,
        "examples": spec.examples,
        "complexity": {"time": spec.complexity.time, "space": spec.complexity.space},
        "is_async": spec.is_async,
        "test_count": spec.test_count,
        "meta": {
            "name": spec.meta.name,
            "language": spec.meta.language,
            "version": spec.meta.version,
            "tags": spec.meta.tags,
            "agent": spec.meta.agent,
            "mcp_server": spec.meta.mcp_server,
        },
    }


async def _validate_rune_spec(filepath: str, strict: bool = False) -> dict[str, Any]:
    """Validate a .rune file and return a report."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return {
            "valid": False,
            "filepath": filepath,
            "errors": ["File is empty"],
            "warnings": [],
        }

    errors: list[str] = []
    warnings: list[str] = []

    try:
        spec = _parser.parse_string(content)
    except ParseError as exc:
        return {
            "valid": False,
            "filepath": filepath,
            "errors": [str(exc)],
            "warnings": [],
        }

    # Structural validation
    validation_errors = _parser.validate(spec)
    errors.extend(validation_errors)

    # Quality checks
    if spec.test_count < 3:
        warnings.append(f"Only {spec.test_count} test(s); recommended minimum is 3")

    has_when_then = any("WHEN" in b and "THEN" in b for b in spec.behavior)
    if not has_when_then and spec.behavior:
        warnings.append("BEHAVIOR does not use WHEN/THEN format")

    if strict:
        if not spec.edge_cases:
            warnings.append("Missing EDGE_CASES section (required in strict mode)")
        if not spec.constraints:
            warnings.append("Missing CONSTRAINTS section (required in strict mode)")
        if not spec.examples:
            warnings.append("Missing EXAMPLES section (required in strict mode)")
        if not spec.complexity.time and not spec.complexity.space:
            warnings.append("Missing COMPLEXITY section (required in strict mode)")

    return {
        "valid": len(errors) == 0,
        "filepath": filepath,
        "errors": errors,
        "warnings": warnings,
    }


async def _list_rune_specs(directory: str) -> list[dict[str, str]]:
    """List all .rune files in a directory."""
    dirpath = Path(directory)
    if not dirpath.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    results = []
    for rune_file in sorted(dirpath.rglob("*.rune")):
        try:
            spec = _parser.parse_file(rune_file)
            results.append({
                "filepath": str(rune_file),
                "name": spec.name,
                "language": spec.language,
                "intent": spec.intent[:120] + "..." if len(spec.intent) > 120 else spec.intent,
                "test_count": str(spec.test_count),
            })
        except (ParseError, Exception) as exc:
            results.append({
                "filepath": str(rune_file),
                "name": "",
                "language": "",
                "intent": f"(parse error: {exc})",
                "test_count": "0",
            })

    return results


# ---------------------------------------------------------------------------
# MCP tool registration
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="parse_rune_spec",
            description="Parse a .rune specification file and return its structured contents",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the .rune file to parse",
                    },
                },
                "required": ["filepath"],
            },
        ),
        Tool(
            name="validate_rune_spec",
            description="Validate a .rune file against RUNE specification standards",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the .rune file to validate",
                    },
                    "strict": {
                        "type": "boolean",
                        "description": "Enable strict mode (check optional fields)",
                        "default": False,
                    },
                },
                "required": ["filepath"],
            },
        ),
        Tool(
            name="list_rune_specs",
            description="List all .rune specification files in a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path to search for .rune files",
                    },
                },
                "required": ["directory"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "parse_rune_spec":
        result = await _parse_rune_spec(arguments["filepath"])
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    if name == "validate_rune_spec":
        result = await _validate_rune_spec(
            arguments["filepath"],
            strict=arguments.get("strict", False),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    if name == "list_rune_specs":
        result = await _list_rune_specs(arguments["directory"])
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    raise ValueError(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
