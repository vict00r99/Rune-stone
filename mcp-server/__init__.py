"""
Runestone MCP Server

An MCP server that exposes RUNE spec parsing and validation as tools.
AI assistants can use these tools to read, validate, and work with
RUNE specifications directly.

Usage:
    python -m mcp_server
"""

from .parser import RUNEParser, parse_rune_file, parse_rune_string
from .server import server

__all__ = ["RUNEParser", "parse_rune_file", "parse_rune_string", "server"]
