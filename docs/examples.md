# RUNE Examples

## Start Here

### [Full Pipeline](../examples/full-project/) — Requirements to specs to code

The complete RUNE workflow for an online bookstore:

1. **REQUIREMENTS.md** — Business requirements written by an analyst
2. **specs/*.rune** — YAML specs generated from requirements
3. **src/*.py** — Python implementations generated from specs
4. **tests/*.py** — Tests generated from specs

Functions: `calculate_order_total`, `validate_coupon`, `check_free_shipping`

---

## More Examples

### [RUNE inside AGENTS.md](../examples/integrations/agents-md-with-rune/)

Same three bookstore functions, but as **Markdown sections** embedded in an AGENTS.md file instead of standalone `.rune` files. Shows how the two formats coexist.

### [Multi-Language](../examples/multi-language/)

One `slugify.rune` spec (`language: any`) implemented in both **Python** and **TypeScript** with full test suites. Proves the same spec produces consistent behavior across languages.

### [Basic Specs](../examples/basic/)

Three simple standalone specs with reference implementations:

| Spec | What it shows | Impl |
|------|--------------|------|
| `is_shop_open.rune` | Boolean logic, business rules, boundary conditions | `is_shop_open.py` |
| `validate_email.rune` | String validation, tuple returns, multiple error paths | `validate_email.py` |
| `calculate_discount.rune` | Numeric calculations, range validation, precision | `calculate_discount.py` |

---

## Integration Examples

### [agents.md + Multi-Agent System](../examples/integrations/agents-md-example/)

Agent architecture (`agents.md`) with RUNE-specified tools (`test_validator.rune`, `doc_generator.rune`). Shows how agents.md defines *who does what* while RUNE defines *how each tool works*.

### [MCP Server](../examples/integrations/mcp-example/)

MCP server with RUNE-specified async tools (`search_documents.rune`, `file_operations.rune`). Includes a working `server.py`.

### [Claude Projects](../examples/integrations/claude-project-example/)

Example Claude Project setup with `project_instructions.md` and RUNE specs (`api_client.rune`, `data_validator.rune`).

---

## Templates

Starter templates for writing specs manually. Located in [`templates/`](../templates/).

| Template | Use for |
|----------|---------|
| `basic-function.rune` | Standard synchronous function |
| `async-function.rune` | Async/await with timeout handling |
| `class-spec.rune` | Class with multiple methods |
| `agent-tool.rune` | Agent system tool |
| `mcp-tool.rune` | MCP server tool |

**Note:** You don't need templates if you use AI to generate specs. The skill file (`rune-writer.md`) already teaches the AI the complete pattern. Templates are reference material for manual writing.

---

## Resources

- [Getting Started](getting-started.md) — 5-minute tutorial
- [Workflow Guide](workflow.md) — Team adoption and analyst/developer workflow
- [Before & After](before-after.md) — Side-by-side comparison
- [SPEC.md](../SPEC.md) — Full pattern reference
- [Best Practices](best-practices.md) — Writing guidelines
