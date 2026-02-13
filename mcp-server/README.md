# Runestone MCP Server

An MCP server that exposes RUNE spec parsing and validation as tools for AI assistants.

## Tools

| Tool | Description |
|------|-------------|
| `parse_rune_spec` | Parse a `.rune` file and return structured data |
| `validate_rune_spec` | Validate a `.rune` file against SPEC.md standards |
| `list_rune_specs` | List all `.rune` files in a directory |

## Setup

### Install

```bash
cd mcp-server
pip install -e .
```

Or install dependencies directly:

```bash
pip install "mcp>=1.0.0" "pyyaml>=6.0"
```

### Run

```bash
python -m mcp_server
```

### Configure for Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "runestone": {
      "command": "python",
      "args": ["-m", "mcp_server"]
    }
  }
}
```

## Usage

Once connected, an AI assistant can:

```
# Parse a spec to understand its contents
parse_rune_spec(filepath="examples/basic/calculate_discount.rune")

# Validate a spec for correctness
validate_rune_spec(filepath="examples/basic/validate_email.rune", strict=true)

# List all specs in a project
list_rune_specs(directory="examples/")
```

## Python API

The parser can also be used directly in Python:

```python
from mcp_server.parser import parse_rune_file, parse_rune_string, RUNEParser

# Parse from file
spec = parse_rune_file("examples/basic/calculate_discount.rune")
print(spec.name)        # "calculate_discount"
print(spec.language)    # "python"
print(spec.signature)   # "def calculate_discount(price: float, percentage: int) -> float"
print(spec.test_count)  # 15
print(spec.is_async)    # False

# Parse from string
spec = parse_rune_string(yaml_content)

# Validate
parser = RUNEParser()
spec = parser.parse_file("my_spec.rune")
errors = parser.validate(spec)
if errors:
    for err in errors:
        print(f"  {err}")
```

## Project Structure

```
mcp-server/
├── __init__.py        # Package exports
├── __main__.py        # Entry point for python -m mcp_server
├── parser.py          # RUNE spec parser and data classes
├── server.py          # MCP server with tool registration
├── pyproject.toml     # Python package configuration
└── README.md          # This file
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/test_parser.py
```
