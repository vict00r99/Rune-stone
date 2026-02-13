# Integrating RUNE with MCP Servers

This guide shows how to use RUNE specifications to define clear contracts for Model Context Protocol (MCP) server tools.

## Overview

**MCP (Model Context Protocol)** allows AI assistants to interact with external tools and data sources. RUNE helps you:

- Define MCP tool contracts before implementation
- Ensure consistent tool interfaces
- Document tool behavior comprehensively
- Test tools thoroughly

## Why Use RUNE with MCP?

| Without RUNE | With RUNE |
|-------------|-----------|
| Tool behavior implicit | Explicit specification |
| Inconsistent interfaces | Standard structure |
| Limited testing | Comprehensive test cases |
| Poor documentation | Self-documenting tools |
| Hard to review | Review specs before code |

## Quick Start

### Step 1: Define Your MCP Tool as a RUNE Spec

Create a spec for your MCP tool:

```yaml
# search_documents.rune
---
meta:
  name: search_documents
  language: python
  version: 1.0
  tags: [mcp-tool, search, documents]
  mcp_server: document_server
---

RUNE: search_documents

SIGNATURE: |
  async def search_documents(
      query: str,
      max_results: int = 10
  ) -> list[dict[str, Any]]

INTENT: |
  MCP tool that searches indexed documents using semantic search.
  Returns ranked results with relevance scores.

BEHAVIOR:
  - WHEN query is empty THEN raise ValueError("Query cannot be empty")
  - WHEN max_results < 1 or > 100 THEN raise ValueError
  - PERFORM semantic search on document index
  - RANK results by relevance score
  - RETURN top max_results documents

CONSTRAINTS:
  - "query: non-empty string, max 500 chars"
  - "max_results: 1-100 inclusive"

EDGE_CASES:
  - "empty query: raises ValueError"
  - "no matches found: returns []"
  - "max_results = 1: returns single result"

TESTS:
  - "await search_documents('python') returns list"
  - "await search_documents('') raises ValueError"
  - "await search_documents('test', 0) raises ValueError"

DEPENDENCIES:
  - "mcp>=0.1.0"
  - "sentence-transformers>=2.0.0"
```

### Step 2: Generate Implementation

Use AI to generate the tool implementation:

```python
# generated from search_documents.rune
async def search_documents(
    query: str,
    max_results: int = 10
) -> list[dict[str, Any]]:
    """
    MCP tool that searches indexed documents using semantic search.
    Returns ranked results with relevance scores.
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    if max_results < 1 or max_results > 100:
        raise ValueError("max_results must be between 1 and 100")
    
    # Semantic search implementation
    results = await perform_semantic_search(query)
    ranked = rank_by_relevance(results)
    
    return ranked[:max_results]
```

### Step 3: Register as MCP Tool

Register the implementation in your MCP server:

```python
from mcp.server.lowlevel import Server
from .tools import search_documents

server = Server("document-server")

@server.tool(
    name="search_documents",
    description="Search indexed documents (see search_documents.rune)"
)
async def search_tool(query: str, max_results: int = 10):
    return await search_documents(query, max_results)
```

## MCP Tool Patterns

### Pattern 1: Query Tool

Tools that search or retrieve data:

```yaml
RUNE: query_database

SIGNATURE: |
  async def query_database(
      sql: str,
      params: dict | None = None,
      timeout: int = 30
  ) -> list[dict]

BEHAVIOR:
  - VALIDATE SQL syntax
  - SANITIZE inputs to prevent injection
  - EXECUTE query with timeout
  - WHEN timeout exceeded THEN raise TimeoutError
  - RETURN query results as list of dicts
```

### Pattern 2: Action Tool

Tools that perform operations:

```yaml
RUNE: send_email

SIGNATURE: |
  async def send_email(
      to: str,
      subject: str,
      body: str,
      attachments: list[str] | None = None
  ) -> dict[str, Any]

BEHAVIOR:
  - VALIDATE email address format
  - VALIDATE attachments exist
  - CONSTRUCT email message
  - SEND via SMTP
  - RETURN status with message_id
```

### Pattern 3: Analysis Tool

Tools that process and analyze data:

```yaml
RUNE: analyze_sentiment

SIGNATURE: |
  async def analyze_sentiment(
      text: str,
      language: str = "en"
  ) -> dict[str, float]

BEHAVIOR:
  - VALIDATE text is non-empty
  - DETECT language if not specified
  - PERFORM sentiment analysis
  - CALCULATE scores (positive, negative, neutral)
  - RETURN scores dictionary
```

## Best Practices for MCP Tools

### 1. Use Async Signatures

MCP tools should be async:

```yaml
✅ Good:
SIGNATURE: async def tool_name(param: str) -> Result

❌ Bad:
SIGNATURE: def tool_name(param: str) -> Result
```

### 2. Include Timeout Handling

```yaml
BEHAVIOR:
  - WHEN operation exceeds timeout THEN raise TimeoutError
  - WHEN network fails THEN raise ConnectionError
  - WHEN rate limited THEN raise RateLimitError
```

### 3. Return Structured Data

Always return structured, predictable data:

```yaml
✅ Good:
SIGNATURE: |
  async def get_weather(city: str) -> dict[str, Any]
  # Returns: {"temp": 72, "conditions": "sunny", "humidity": 45}

❌ Bad:
SIGNATURE: |
  async def get_weather(city: str) -> Any
  # Returns: sometimes dict, sometimes string, sometimes None
```

### 4. Document in meta.mcp_server

Link tool to its server:

```yaml
meta:
  name: search_documents
  language: python
  mcp_server: document_server  # ← Server name
```

### 5. Comprehensive Error Handling

```yaml
BEHAVIOR:
  - WHEN input validation fails THEN raise ValueError
  - WHEN resource not found THEN raise NotFoundError
  - WHEN permission denied THEN raise PermissionError
  - WHEN rate limit exceeded THEN raise RateLimitError
  - WHEN timeout THEN raise TimeoutError
  - WHEN unexpected error THEN raise RuntimeError with details
```

## Complete MCP Server Example

### Directory Structure

```
mcp-server/
├── server.py           # MCP server definition
├── tools/              # RUNE specifications
│   ├── search.rune
│   ├── create.rune
│   └── update.rune
└── implementations/    # Generated from RUNE specs
    ├── search.py
    ├── create.py
    └── update.py
```

### Server Implementation

```python
# server.py
from mcp.server.lowlevel import Server
from .implementations import search_documents, create_document, update_document

server = Server("document-server")

# Register tools (implementations from RUNE specs)
@server.tool(name="search", description="Search documents")
async def search(query: str, max_results: int = 10):
    return await search_documents(query, max_results)

@server.tool(name="create", description="Create document")
async def create(title: str, content: str):
    return await create_document(title, content)

@server.tool(name="update", description="Update document")
async def update(doc_id: str, updates: dict):
    return await update_document(doc_id, updates)

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())
```

## Integration Workflow

### 1. Design Phase

Create RUNE specs for all tools:

```bash
mcp-server/tools/
├── search_documents.rune
├── get_document.rune
├── create_document.rune
├── update_document.rune
└── delete_document.rune
```

### 2. Review Phase

Team reviews specs before implementation:
- Are tool interfaces clear?
- Are error cases handled?
- Are constraints appropriate?
- Is documentation complete?

### 3. Implementation Phase

Generate code from specs:

```bash
# With Claude
for spec in tools/*.rune; do
    claude "Generate implementation from $spec"
done
```

### 4. Testing Phase

Run tests from RUNE specs:

```python
# tests/test_search.py
import pytest
from implementations.search import search_documents

@pytest.mark.asyncio
async def test_search_valid_query():
    results = await search_documents("python")
    assert isinstance(results, list)

@pytest.mark.asyncio
async def test_search_empty_query():
    with pytest.raises(ValueError):
        await search_documents("")
```

### 5. Deploy Phase

Package and deploy MCP server with validated tools.

## Testing MCP Tools

### Unit Tests from RUNE Specs

```python
# Generate tests directly from TESTS section
import pytest
from implementations.search import search_documents

class TestSearchDocuments:
    @pytest.mark.asyncio
    async def test_valid_query(self):
        """From: await search_documents('python') returns list"""
        result = await search_documents('python')
        assert isinstance(result, list)
    
    @pytest.mark.asyncio
    async def test_empty_query(self):
        """From: await search_documents('') raises ValueError"""
        with pytest.raises(ValueError):
            await search_documents('')
    
    @pytest.mark.asyncio
    async def test_invalid_max_results(self):
        """From: await search_documents('test', 0) raises ValueError"""
        with pytest.raises(ValueError):
            await search_documents('test', 0)
```

### Integration Tests

Test tools in MCP context:

```python
@pytest.mark.asyncio
async def test_mcp_tool_search():
    from mcp.client import Client
    
    client = Client("document-server")
    result = await client.call_tool("search", query="python")
    
    assert result["success"]
    assert isinstance(result["data"], list)
```

## Advanced Patterns

### Pattern: Tool with Progress Updates

```yaml
RUNE: process_large_file

SIGNATURE: |
  async def process_large_file(
      filepath: str,
      callback: Callable[[float], None] | None = None
  ) -> ProcessResult

BEHAVIOR:
  - OPEN file for reading
  - FOR each chunk in file
    - PROCESS chunk
    - IF callback provided THEN call with progress percentage
  - RETURN processing result

EXAMPLES:
  - |
    async def progress_handler(percent: float):
        print(f"Progress: {percent}%")
    
    result = await process_large_file(
        "large.csv",
        callback=progress_handler
    )
```

### Pattern: Tool with Streaming Response

```yaml
RUNE: stream_search_results

SIGNATURE: |
  async def stream_search_results(
      query: str
  ) -> AsyncIterator[SearchResult]

BEHAVIOR:
  - VALIDATE query
  - START search operation
  - FOR each result as it arrives
    - YIELD result
  - WHEN all results processed THEN complete

EXAMPLES:
  - |
    async for result in stream_search_results("python"):
        print(f"Found: {result['title']}")
```

### Pattern: Tool with Resource Cleanup

```yaml
RUNE: connect_database

SIGNATURE: |
  async def connect_database(
      connection_string: str
  ) -> AsyncContextManager[Connection]

BEHAVIOR:
  - VALIDATE connection string
  - ESTABLISH database connection
  - RETURN async context manager
  - ON exit THEN close connection properly

EXAMPLES:
  - |
    async with connect_database(conn_str) as db:
        results = await db.query("SELECT * FROM users")
```

## Troubleshooting

### Issue: Tool fails with unexpected input

**Check RUNE spec:**
- Are CONSTRAINTS documented?
- Are EDGE_CASES handled?
- Does implementation validate inputs?

### Issue: Tool behavior unclear

**Update RUNE spec:**
- Make BEHAVIOR more explicit
- Add more EXAMPLES
- Document edge cases

### Issue: Tool tests incomplete

**Review TESTS section:**
- Add happy path tests
- Add boundary tests
- Add error case tests

## Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Example MCP Server](../examples/integrations/mcp-example/)
- [RUNE Templates](../templates/mcp-tool.rune)

## Next Steps

1. Review [complete MCP example](../examples/integrations/mcp-example/)
2. Create RUNE specs for your MCP tools
3. Generate implementations
4. Test thoroughly
5. Deploy your MCP server

---

**Build better MCP servers with RUNE!** 🗿