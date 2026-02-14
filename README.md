# Runestone

**A specification pattern for consistent AI code generation.**

Define function behavior once. Any AI tool generates consistent, tested code with the same behavior — every time, every developer, every language.

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

RUNE is a pattern, not a file format. The same structure (SIGNATURE, BEHAVIOR, TESTS...) can be written as **YAML `.rune` files** for formal specs or as **Markdown sections** inside AGENTS.md. The container changes, the contract doesn't.

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

Same pattern, different container. The AI generates code with the same behavior from both.

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

**1. Load the Writer skill into your AI tool.**

Upload [`skills/rune-writer.md`](skills/rune-writer.md) to Claude Projects, paste it into ChatGPT, add it to `.cursorrules`, or any other method. This teaches the AI the RUNE pattern.

**2. Describe what you need.**

> "I need a function that checks if an order qualifies for free shipping. Orders over $50 get free shipping. Loyalty members always get free shipping."

**3. The AI generates a RUNE spec.**

Review it. Does the BEHAVIOR cover all your rules? Are the TESTS complete? Iterate until the contract is right.

**4. Implement from the spec.**

> "Implement check_free_shipping.rune"

The AI generates code + tests that follow the spec exactly.

## Skills

7 skills for the full lifecycle. Start with the Writer — add others as needed.

| Skill | What it does |
|-------|-------------|
| **[Writer](skills/rune-writer.md)** | Create specs from requirements. Implement code from specs. |
| **[Validator](skills/rune-validator.md)** | Check if a spec is complete and well-formed. |
| **[Refiner](skills/rune-refiner.md)** | Suggest missing tests, edge cases, and clarifications. |
| **[Test Generator](skills/rune-test-generator.md)** | Generate runnable test files from a spec. |
| **[Diff](skills/rune-diff.md)** | Compare spec vs implementation to detect drift. |
| **[From Code](skills/rune-from-code.md)** | Reverse-engineer a spec from existing code. |
| **[Multi-Lang](skills/rune-multi-lang.md)** | Generate implementations in multiple languages from one spec. |

Copy [`AGENTS.md`](AGENTS.md) into your project as a reference for your AI tools.

## Examples

- **[Full pipeline](examples/full-project/)** — Requirements to specs to code (start here)
- **[Multi-language](examples/multi-language/)** — Same spec in Python + TypeScript
- **[RUNE inside AGENTS.md](examples/integrations/agents-md-with-rune/)** — Specs embedded in markdown
- **[Basic specs](examples/basic/)** — Simple functions with implementations
- **[MCP tools](examples/integrations/mcp-example/)** — Async tool specifications

## Documentation

- **[Getting Started](docs/getting-started.md)** — Quick tutorial
- **[Workflow Guide](docs/workflow.md)** — Complete guide with all skills
- **[Before & After](docs/before-after.md)** — Side-by-side comparison
- **[SPEC.md](SPEC.md)** — Full pattern reference
- **[Best Practices](docs/best-practices.md)** — Writing guidelines
- **[Templates](templates/)** — Starter templates for manual writing

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
