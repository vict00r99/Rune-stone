# RUNE Templates

Starter templates for writing RUNE specs **manually** in YAML format.

## When to use templates

**You probably don't need them.** If you use AI with the skill file (`skills/rune-writer.md`), the AI generates complete specs from your requirements — no template needed.

Templates are useful if you:
- Prefer writing specs by hand
- Want to see the YAML structure as a reference
- Are setting up a new project and want a starting point

## Available templates

| Template | Use for |
|----------|---------|
| `basic-function.rune` | Standard synchronous function |
| `async-function.rune` | Async/await function with timeout handling |
| `class-spec.rune` | Class with multiple methods |
| `agent-tool.rune` | Tool for an agent system |
| `mcp-tool.rune` | MCP server tool |

## Writing specs in Markdown instead?

If you prefer the Markdown format (e.g., embedding specs in AGENTS.md), you don't need a template file. The structure is straightforward:

```markdown
### function_name

**SIGNATURE:** `def function_name(param: type) -> return_type`

**INTENT:** What the function does in 1-3 sentences.

**BEHAVIOR:**
- WHEN condition THEN action
- OTHERWISE default_action

**TESTS:**
- `function_name(input) == expected`
- `function_name(bad_input) raises ValueError`

**EDGE_CASES:**
- boundary condition: expected behavior
```

See [SPEC.md](../SPEC.md) for the full pattern reference.
