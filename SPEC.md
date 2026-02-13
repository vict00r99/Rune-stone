# RUNE Specification v1.1

**RUNE** is a specification pattern for defining function behavior before AI-assisted implementation.

## Purpose

RUNE provides a structured contract between human intent and AI implementation, ensuring consistent code generation, comprehensive tests, and explicit edge case handling.

RUNE is format-agnostic. The same pattern works as:
- **YAML** — standalone `.rune` files (parseable, validatable)
- **Markdown** — sections embedded in AGENTS.md, README.md, or any document

## The Pattern

Every RUNE spec must include these required fields:

| Field | Required | Description |
|-------|----------|-------------|
| **SIGNATURE** | Yes | Function declaration in target language syntax |
| **INTENT** | Yes | What it does (1-3 sentences, docstring-ready) |
| **BEHAVIOR** | Yes | Logic rules in WHEN/THEN/OTHERWISE format |
| **TESTS** | Yes | Minimum 3 test cases (happy path, boundary, error) |
| CONSTRAINTS | No | Input validation rules and preconditions |
| EDGE_CASES | No | Boundary conditions and expected behavior |
| DEPENDENCIES | No | External libraries required |
| EXAMPLES | No | Usage examples |
| COMPLEXITY | No | Big-O time/space notation |

---

## Format A: YAML (.rune files)

Standalone files for formal, parseable specifications. Includes a `meta` header for tooling.

```yaml
---
meta:
  name: function_name          # Required: identifier
  language: python             # Required: target language
  version: 1.0                 # Optional: spec version
  tags: [category, tags]       # Optional: labels
---

RUNE: function_name

SIGNATURE: |
  def function_name(param: type) -> return_type

INTENT: |
  Clear 1-3 sentence description of purpose.

BEHAVIOR:
  - WHEN condition THEN action
  - WHEN another_condition THEN another_action
  - OTHERWISE default_action

TESTS:
  - "function_name(input) == expected"
  - "function_name(boundary) == expected"
  - "function_name(invalid) raises ValueError"

CONSTRAINTS:
  - "param: must be >= 0"

EDGE_CASES:
  - "empty input: returns empty result"

DEPENDENCIES:
  - "library>=1.0.0"

EXAMPLES:
  - |
    result = function_name(input)
    # Returns: expected

COMPLEXITY:
  time: O(n)
  space: O(1)
```

### YAML-specific fields

- **meta.name** (required): Function/module identifier
- **meta.language** (required): Target language (python, typescript, go, rust, java, etc.)
- **meta.version**: Spec version (defaults to 1.0)
- **meta.tags**: Categorization labels
- **meta.agent**: Agent name for agents.md integration
- **meta.mcp_server**: Server name for MCP integration
- **RUNE**: The function/class name (must match meta.name)

### Editor Configuration

Configure editors to treat `.rune` as YAML:

**VS Code** — `settings.json`:
```json
{ "files.associations": { "*.rune": "yaml" } }
```

**Neovim/Vim**:
```vim
autocmd BufNewFile,BufRead *.rune set filetype=yaml
```

---

## Format B: Markdown (embedded specs)

Sections inside any `.md` file. No special tooling needed.

```markdown
### function_name

**SIGNATURE:** `def function_name(param: type) -> return_type`

**INTENT:** Clear 1-3 sentence description of purpose.

**BEHAVIOR:**
- WHEN condition THEN action
- WHEN another_condition THEN another_action
- OTHERWISE default_action

**TESTS:**
- `function_name(input) == expected`
- `function_name(boundary) == expected`
- `function_name(invalid) raises ValueError`

**CONSTRAINTS:**
- param: must be >= 0

**EDGE_CASES:**
- empty input: returns empty result
```

### Embedding in AGENTS.md

Add a `## Function Specifications` section to your AGENTS.md:

```markdown
# AGENTS.md

## Project Context
Python 3.11, pytest, hexagonal architecture.

## Function Specifications

### calculate_order_total
**SIGNATURE:** `def calculate_order_total(items: list[dict], tax_rate: float) -> float`
**INTENT:** Calculates order total including tax.
**BEHAVIOR:**
- WHEN items is empty THEN return 0.00
- WHEN any item has price <= 0 THEN raise ValueError
- CALCULATE subtotal + tax, round to 2 decimals
**TESTS:**
- `calculate_order_total([{'price': 15.99, 'quantity': 2}], 8.5) == 34.70`
- `calculate_order_total([], 8.5) == 0.00`
- `calculate_order_total([{'price': -5, 'quantity': 1}], 8.5) raises ValueError`
```

---

## Field Reference

### SIGNATURE (required)

The exact function declaration in the target language's syntax. Not pseudocode.

```
Python:     def calculate_discount(price: float, percentage: int) -> float
TypeScript: function calculateDiscount(price: number, percentage: number): number
Go:         func CalculateDiscount(price float64, percentage int) float64
Rust:       fn calculate_discount(price: f64, percentage: i32) -> f64
```

For language-agnostic specs, use a neutral format:
```
function calculate_discount(price: float, percentage: int) -> float
```

### INTENT (required)

1-3 sentences. Must be clear enough to serve as a docstring. Describes the "what", not the "how".

### BEHAVIOR (required)

Each business rule as a WHEN/THEN clause. Use OTHERWISE for the default case.

```
- WHEN input is invalid THEN raise error with specific message
- WHEN condition A THEN action A
- WHEN condition B THEN action B
- OTHERWISE default action
```

Order matters — rules are evaluated top to bottom. Put validations first, business logic second, default last.

### TESTS (required)

Minimum 3 test cases covering:
1. **Happy path** — normal, expected input
2. **Boundary** — edge values (0, empty, max, exactly-at-threshold)
3. **Error** — invalid input that should fail

Format: `function(input) == expected` or `function(invalid) raises ErrorType`

### CONSTRAINTS (optional)

Input validation rules. Each constraint maps to a validation check in the implementation.

### EDGE_CASES (optional)

Boundary conditions with expected behavior. Each should have a corresponding test.

### DEPENDENCIES, EXAMPLES, COMPLEXITY (optional)

Supporting information for implementation.

---

## Validation Rules

A valid RUNE spec must:
1. Include all required fields (SIGNATURE, INTENT, BEHAVIOR, TESTS)
2. Have SIGNATURE in actual language syntax
3. Have BEHAVIOR using WHEN/THEN format
4. Have at least 3 test cases
5. Have INTENT of 1-3 sentences
6. If YAML: valid YAML, meta.name and meta.language present
7. If Markdown: bold field names, code in backticks

## Best Practices

See [docs/best-practices.md](docs/best-practices.md) for writing guidelines.

## Integration Guides

- **[AGENTS.md + RUNE](docs/integration-agents-md.md)** — Embed specs in AGENTS.md
- **[MCP Server](docs/integration-mcp.md)** — Specify MCP tool contracts
- **[AI Tool Setup](docs/using-skills-with-other-tools.md)** — Claude, Cursor, Aider, Copilot, etc.

## Version History

- **v1.1** (2026-02-13): Dual format support (YAML + Markdown), pattern-first positioning
- **v1.0** (2025): Initial YAML-only specification

## License

MIT License. RUNE is an open standard — use, extend, and build on it freely.
