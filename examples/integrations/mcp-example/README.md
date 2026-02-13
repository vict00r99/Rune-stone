# MCP Server Integration Example

A complete Model Context Protocol (MCP) server with tools defined by RUNE specifications.

## What This Demonstrates

- Defining MCP tool contracts as RUNE specs before implementation
- Implementing a working MCP server from those specs
- Registering tools with proper JSON Schema input definitions
- Input validation, error handling, and structured responses

## Files

| File | Description |
|------|-------------|
| `search_documents.rune` | RUNE spec for the semantic search tool |
| `file_operations.rune` | RUNE spec for the file reading tool |
| `server.py` | Complete MCP server implementing both tools |

## Tools

### search_documents

Searches an indexed document collection using keyword matching (swap in a vector DB for production). Supports filtering by date range, tags, and author.

```python
results = await search_documents("python async", max_results=5)
```

### read_file

Reads file contents with size limits, encoding support, and path traversal protection.

```python
result = await read_file("docs/readme.md", max_bytes=4096)
```

## Setup

### Prerequisites

```bash
pip install "mcp>=1.0.0"
```

For production semantic search, also install:

```bash
pip install "chromadb>=0.4.0" "sentence-transformers>=2.2.0"
```

### Run the Server

```bash
python server.py
```

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```

### Configure for Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "runestone-example": {
      "command": "python",
      "args": ["path/to/examples/integrations/mcp-example/server.py"],
      "env": {
        "RUNE_SANDBOX_ROOT": "/path/to/allowed/directory"
      }
    }
  }
}
```

## Development Workflow

1. **Design** -- Write RUNE specs for each tool
2. **Review** -- Validate specs cover all edge cases and error conditions
3. **Implement** -- Build `server.py` following the specs exactly
4. **Test** -- Verify all TESTS from the specs pass
5. **Deploy** -- Register the MCP server with your AI assistant

## Extending This Example

To add a new tool:

1. Create a `.rune` spec file defining the tool contract
2. Implement the async tool function in `server.py` following the spec
3. Add a `Tool` entry in `list_tools()` with a JSON Schema
4. Handle the tool name in `call_tool()`
5. Test all cases from the TESTS section

## Related

- [RUNE + MCP Integration Guide](../../../docs/integration-mcp.md)
- [MCP Tool Template](../../../templates/mcp-tool.rune)
- [RUNE Specification](../../../SPEC.md)
