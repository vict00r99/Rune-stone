"""
Runestone MCP Server Example

A complete MCP server implementation with tools defined by RUNE specifications.
Tools: search_documents (search_documents.rune), read_file (file_operations.rune)

Usage:
    python server.py
    # Or with MCP inspector:
    npx @modelcontextprotocol/inspector python server.py
"""

from __future__ import annotations

import asyncio
import codecs
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.lowlevel import Server
import mcp.server.stdio
from mcp.types import TextContent, Tool

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SANDBOX_ROOT = Path(os.environ.get("RUNE_SANDBOX_ROOT", ".")).resolve()
MAX_QUERY_LENGTH = 500
MAX_RESULTS_UPPER = 100
CONTENT_PREVIEW_LENGTH = 200
VALID_FILTER_KEYS = {"date_from", "date_to", "tags", "author"}
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# ---------------------------------------------------------------------------
# In-memory document store (replace with ChromaDB in production)
# ---------------------------------------------------------------------------

DOCUMENTS: list[dict[str, Any]] = [
    {
        "id": "doc-001",
        "title": "Getting Started with Python Async",
        "content": (
            "Python's asyncio module provides infrastructure for writing "
            "single-threaded concurrent code using coroutines. This guide "
            "covers the basics of async/await syntax, event loops, and "
            "common patterns for building asynchronous applications."
        ),
        "metadata": {
            "author": "alice",
            "tags": ["python", "async", "tutorial"],
            "date": "2024-06-15",
        },
    },
    {
        "id": "doc-002",
        "title": "MCP Server Development Guide",
        "content": (
            "The Model Context Protocol allows AI assistants to interact "
            "with external tools and data sources. This document covers "
            "server setup, tool registration, and best practices for "
            "building reliable MCP servers."
        ),
        "metadata": {
            "author": "bob",
            "tags": ["mcp", "server", "guide"],
            "date": "2024-09-01",
        },
    },
    {
        "id": "doc-003",
        "title": "RUNE Specification Overview",
        "content": (
            "RUNE is a specification pattern for AI-assisted code "
            "generation. It can be written as YAML (.rune files) or as "
            "Markdown sections in any .md file. It provides a structured "
            "contract between human intent and AI implementation, ensuring "
            "consistent output, comprehensive tests, and clear edge-case handling."
        ),
        "metadata": {
            "author": "alice",
            "tags": ["rune", "specification", "pattern"],
            "date": "2025-01-10",
        },
    },
    {
        "id": "doc-004",
        "title": "Testing Strategies for Python Projects",
        "content": (
            "Effective testing requires a mix of unit tests, integration "
            "tests, and end-to-end tests. This article discusses pytest "
            "fixtures, parametrized tests, mocking strategies, and how "
            "to measure meaningful code coverage."
        ),
        "metadata": {
            "author": "carol",
            "tags": ["python", "testing", "pytest"],
            "date": "2024-11-20",
        },
    },
]


def _relevance_score(query: str, doc: dict[str, Any]) -> float:
    """Compute keyword-overlap relevance score in [0, 1]."""
    terms = set(query.lower().split())
    title_terms = set(doc["title"].lower().split())
    content_terms = set(doc["content"].lower().split())

    if not terms:
        return 0.0

    title_hits = len(terms & title_terms)
    content_hits = len(terms & content_terms)
    raw = (title_hits * 3 + content_hits) / (len(terms) * 4)
    return min(round(raw, 4), 1.0)


def _matches_filters(doc: dict[str, Any], filters: dict[str, Any]) -> bool:
    """Return True if doc passes all filters."""
    meta = doc.get("metadata", {})
    if "date_from" in filters and meta.get("date", "") < filters["date_from"]:
        return False
    if "date_to" in filters and meta.get("date", "") > filters["date_to"]:
        return False
    if "tags" in filters:
        if not set(filters["tags"]).issubset(set(meta.get("tags", []))):
            return False
    if "author" in filters and meta.get("author", "") != filters["author"]:
        return False
    return True


# ---------------------------------------------------------------------------
# Tool: search_documents  (spec: search_documents.rune)
# ---------------------------------------------------------------------------

async def search_documents(
    query: str,
    max_results: int = 10,
    filters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Search indexed documents using semantic search.

    Implements the contract defined in search_documents.rune.
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(f"Query exceeds {MAX_QUERY_LENGTH} character limit")
    if max_results < 1:
        raise ValueError("max_results must be at least 1")
    if max_results > MAX_RESULTS_UPPER:
        raise ValueError(f"max_results must be at most {MAX_RESULTS_UPPER}")

    if filters is not None:
        invalid = set(filters.keys()) - VALID_FILTER_KEYS
        if invalid:
            raise ValueError(f"Invalid filter keys: {invalid}")
        for key in ("date_from", "date_to"):
            if key in filters and not ISO_DATE_RE.match(filters[key]):
                raise ValueError("Dates must be ISO 8601 format")
        if "date_from" in filters and "date_to" in filters:
            if filters["date_from"] > filters["date_to"]:
                raise ValueError("date_from must not be after date_to")

    scored: list[tuple[float, dict[str, Any]]] = []
    for doc in DOCUMENTS:
        if filters and not _matches_filters(doc, filters):
            continue
        score = _relevance_score(query, doc)
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda pair: pair[0], reverse=True)

    results: list[dict[str, Any]] = []
    for score, doc in scored[:max_results]:
        preview = doc["content"][:CONTENT_PREVIEW_LENGTH]
        if len(doc["content"]) > CONTENT_PREVIEW_LENGTH:
            preview += "..."
        results.append({
            "id": doc["id"],
            "title": doc["title"],
            "content_preview": preview,
            "score": score,
            "metadata": doc["metadata"],
        })
    return results


# ---------------------------------------------------------------------------
# Tool: read_file  (spec: file_operations.rune)
# ---------------------------------------------------------------------------

async def read_file(
    filepath: str,
    encoding: str = "utf-8",
    max_bytes: int | None = None,
) -> dict[str, Any]:
    """Safely read file contents with metadata.

    Implements the contract defined in file_operations.rune.
    """
    if not filepath:
        raise ValueError("Filepath cannot be empty")
    if ".." in filepath.replace("\\", "/").split("/"):
        raise ValueError("Path traversal not allowed")

    resolved = (SANDBOX_ROOT / filepath).resolve()
    if not str(resolved).startswith(str(SANDBOX_ROOT)):
        raise ValueError("Path traversal not allowed")
    if not resolved.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if not os.access(resolved, os.R_OK):
        raise PermissionError(f"Cannot read file: {filepath}")

    try:
        codecs.lookup(encoding)
    except LookupError:
        raise ValueError(f"Unsupported encoding: {encoding}")

    stat = resolved.stat()
    size_bytes = stat.st_size
    modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()

    truncated = False
    read_size = size_bytes
    if max_bytes is not None and max_bytes > 0 and size_bytes > max_bytes:
        read_size = max_bytes
        truncated = True

    raw = resolved.read_bytes()[:read_size]
    content = raw.decode(encoding)

    return {
        "content": content,
        "filepath": filepath,
        "size_bytes": size_bytes,
        "modified": modified,
        "encoding": encoding,
        "truncated": truncated,
    }


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

server = Server("runestone-example")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_documents",
            description=(
                "Search indexed documents using semantic search. "
                "Supports filtering by date range, tags, and author."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (max 500 chars)",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum results to return (1-100)",
                        "default": 10,
                    },
                    "filters": {
                        "type": "object",
                        "description": "Optional: date_from, date_to, tags, author",
                        "properties": {
                            "date_from": {"type": "string"},
                            "date_to": {"type": "string"},
                            "tags": {"type": "array", "items": {"type": "string"}},
                            "author": {"type": "string"},
                        },
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="read_file",
            description=(
                "Read file contents with metadata. Supports encoding "
                "selection and byte limits for safe file access."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file to read",
                    },
                    "encoding": {
                        "type": "string",
                        "description": "File encoding (default: utf-8)",
                        "default": "utf-8",
                    },
                    "max_bytes": {
                        "type": "integer",
                        "description": "Max bytes to read (null = unlimited)",
                    },
                },
                "required": ["filepath"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "search_documents":
        results = await search_documents(
            query=arguments["query"],
            max_results=arguments.get("max_results", 10),
            filters=arguments.get("filters"),
        )
        return [TextContent(type="text", text=json.dumps(results, indent=2))]

    if name == "read_file":
        result = await read_file(
            filepath=arguments["filepath"],
            encoding=arguments.get("encoding", "utf-8"),
            max_bytes=arguments.get("max_bytes"),
        )
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
