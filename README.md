# Runestone

**A specification pattern for consistent AI code generation.**

Define function behavior once. Any AI tool generates the same consistent, tested implementation — every time, every developer, every language.

---

## The Problem

AI code generation gives different results every time. Ask three developers to build the same function with AI — you get three different implementations. Different error handling, missing tests, forgotten edge cases.

There's no contract between "what I want" and "what AI produces."

## The Solution

RUNE is that contract. A structured pattern that specifies what a function does — its signature, behavior rules, edge cases, and tests. Give it to any AI tool and get the same behavior every time.

```
Requirements  ──▶  RUNE specs  ──▶  Code + Tests
 (Analyst)       (Analyst + AI)   (Developer + AI)
```

RUNE is not a file format — it's a discipline. Write specs as **YAML files** or as **Markdown sections** inside AGENTS.md. The pattern is the same either way.

## Quick Example

A business requirement says: *"Validate coupon codes. Case-insensitive. Check expiration. Return valid/invalid with reason."*

### As a `.rune` file (YAML)

```yaml
RUNE: validate_coupon

SIGNATURE: |
  def validate_coupon(code: str, coupons: list[dict], date: str) -> tuple[bool, str]

BEHAVIOR:
  - WHEN code is empty THEN return (False, "Coupon code cannot be empty")
  - WHEN code not found (case-insensitive) THEN return (False, "Not found")
  - WHEN coupon has expired THEN return (False, "Expired")
  - OTHERWISE return (True, matching_coupon)

TESTS:
  - "validate_coupon('SAVE10', [...], '2025-01-15')[0] == True"
  - "validate_coupon('save10', [...], '2025-01-15')[0] == True"
  - "validate_coupon('', [], '2025-01-15')[0] == False"
  - "validate_coupon('OLD', [...], '2025-01-15')[0] == False"
```

### As a Markdown section (inside AGENTS.md)

```markdown
### validate_coupon

**SIGNATURE:** `def validate_coupon(code: str, coupons: list[dict], date: str) -> tuple[bool, str]`

**BEHAVIOR:**
- WHEN code is empty THEN return (False, "Coupon code cannot be empty")
- WHEN code not found (case-insensitive) THEN return (False, "Not found")
- WHEN coupon has expired THEN return (False, "Expired")
- OTHERWISE return (True, matching_coupon)

**TESTS:**
- `validate_coupon('SAVE10', [...], '2025-01-15')[0] == True`
- `validate_coupon('save10', [...], '2025-01-15')[0] == True`
- `validate_coupon('', [], '2025-01-15')[0] == False`
```

Same pattern, different container. The AI generates the same implementation from both.

## How It Works with AGENTS.md

RUNE complements AGENTS.md — it doesn't replace it.

- **AGENTS.md** defines how the project works (conventions, architecture, tools)
- **RUNE specs** define how each function behaves (signature, rules, tests, edge cases)

You can embed RUNE specs directly inside your AGENTS.md:

```markdown
# AGENTS.md

## Project Context
Python 3.11, pytest, hexagonal architecture.

## Function Specifications

### calculate_order_total
**SIGNATURE:** `def calculate_order_total(items: list[dict], tax_rate: float) -> float`
**BEHAVIOR:**
- WHEN items is empty THEN return 0.00
- WHEN any item has price <= 0 THEN raise ValueError
...
```

Or keep them as separate `.rune` files — whatever fits your workflow.

## Why RUNE?

| Without RUNE | With RUNE |
|-------------|-----------|
| Different code every time | Same behavior, any AI tool |
| No tests until after | Tests defined before code |
| Edge cases forgotten | Edge cases in the contract |
| "It works on my prompt" | Reproducible results |
| Requirements lost in chat | Specs live in the repo |

## Getting Started

**1. Load the skill into your AI tool.**

Upload [`skills/rune-writer.md`](skills/rune-writer.md) to Claude Projects, paste it into ChatGPT, add it to `.cursorrules`, or any other method. This single file teaches the AI the RUNE pattern.

**2. Describe what you need.**

> "I need a function that checks if an order qualifies for free shipping. Orders over $50 get free shipping. Loyalty members always get free shipping."

**3. The AI generates a RUNE spec.**

Review it. Does the BEHAVIOR cover all your rules? Are the TESTS complete? Iterate until the contract is right.

**4. Implement from the spec.**

> "Implement check_free_shipping.rune in Python"

The AI generates code + tests that match the spec exactly.

## Examples

- **[Full pipeline](examples/full-project/)** — Requirements to specs to code (start here)
- **[Multi-language](examples/multi-language/)** — Same spec in Python + TypeScript
- **[RUNE inside AGENTS.md](examples/integrations/agents-md-with-rune/)** — Specs embedded in markdown
- **[Basic specs](examples/basic/)** — Simple functions with implementations
- **[MCP tools](examples/integrations/mcp-example/)** — Async tool specifications

## Documentation

- **[Workflow Guide](docs/workflow.md)** — How analysts generate specs and developers implement them
- **[Getting Started](docs/getting-started.md)** — Quick tutorial
- **[Before & After](docs/before-after.md)** — Side-by-side comparison
- **[SPEC.md](SPEC.md)** — Full pattern reference
- **[Best Practices](docs/best-practices.md)** — Writing guidelines
- **[Templates](templates/)** — Starter templates

## Contributing

RUNE is an open standard. Contributions welcome:

- Submit example specs (YAML or Markdown)
- Build tooling (linters, validators, extensions)
- Write integration guides
- Create language-specific templates

See [SPEC.md](SPEC.md#contributing) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

*Stop generating chaos. Start carving specs in stone.*
