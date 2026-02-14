# AGENTS.md — Runestone

Copy this file to your project and adapt it. It teaches any AI tool how to work with RUNE specifications.

---

## What is RUNE

RUNE is a specification pattern for defining function behavior before implementation. A RUNE spec is a contract: it defines a function's signature, behavior rules, edge cases, and tests. Any AI tool generates code with consistent behavior from the same contract.

Specs can be written as **YAML `.rune` files** or as **Markdown sections** in this file.

## Skills

Runestone provides 7 skills. Each is a standalone `.md` file you can load into any AI tool. Load only the ones you need.

### Core

| Skill | File | When to use |
|-------|------|-------------|
| **Writer** | `skills/rune-writer.md` | Create specs from requirements. Implement code from specs. |
| **Validator** | `skills/rune-validator.md` | Check if a spec is complete and well-formed. |

### Quality

| Skill | File | When to use |
|-------|------|-------------|
| **Refiner** | `skills/rune-refiner.md` | Improve a valid spec: find missing tests, uncovered edge cases, ambiguous rules. |
| **Test Generator** | `skills/rune-test-generator.md` | Generate runnable test files (any framework) from a spec's TESTS section. |

### Lifecycle

| Skill | File | When to use |
|-------|------|-------------|
| **Diff** | `skills/rune-diff.md` | Compare a spec against its implementation to detect drift. |
| **From Code** | `skills/rune-from-code.md` | Reverse-engineer a spec from an existing function. |
| **Multi-Lang** | `skills/rune-multi-lang.md` | Generate implementations in multiple languages from one spec. |

## Workflow

```
          ┌─────────────┐
          │ Requirements │
          └──────┬──────┘
                 ▼
          ┌─────────────┐
          │   Writer     │  Create spec from requirements
          └──────┬──────┘
                 ▼
          ┌─────────────┐
          │  Validator   │  Check structure and rules
          └──────┬──────┘
                 ▼
          ┌─────────────┐
          │   Refiner    │  Suggest improvements
          └──────┬──────┘
                 ▼
    ┌────────────┴────────────┐
    ▼                         ▼
┌─────────┐          ┌──────────────┐
│ Writer   │          │Test Generator │
│(implement)│          │(test files)  │
└────┬─────┘          └──────┬───────┘
     └────────┬──────────────┘
              ▼
       ┌─────────────┐
       │    Diff      │  Audit spec vs code over time
       └─────────────┘
```

**Adopting RUNE on existing code:**
```
Existing function → From Code → spec → Validator → Refiner → done
```

**Multi-language projects:**
```
Spec (language: any) → Multi-Lang → implementations + tests in N languages
```

## Spec Format

### Required fields

Every RUNE spec must have:

- **SIGNATURE** — exact function declaration in the target language's syntax
- **INTENT** — 1-3 sentences describing purpose (no implementation details)
- **BEHAVIOR** — logic rules in WHEN/THEN/OTHERWISE format, evaluated top to bottom
- **TESTS** — minimum 3: happy path, boundary, error

### Optional fields

CONSTRAINTS, EDGE_CASES, DEPENDENCIES, EXAMPLES, COMPLEXITY.

### YAML format (`.rune` files)

```yaml
---
meta:
  name: function_name
  language: python
  version: 1.0
---
RUNE: function_name

SIGNATURE: |
  def function_name(param: type) -> return_type

INTENT: |
  What it does. 1-3 sentences.

BEHAVIOR:
  - WHEN condition THEN action
  - OTHERWISE default_action

TESTS:
  - "function_name(input) == expected"
  - "function_name(boundary) == expected"
  - "function_name(invalid) raises error"
```

### Markdown format (embedded in this file or any `.md`)

```markdown
### function_name

**SIGNATURE:** `def function_name(param: type) -> return_type`

**INTENT:** What it does. 1-3 sentences.

**BEHAVIOR:**
- WHEN condition THEN action
- OTHERWISE default_action

**TESTS:**
- `function_name(input) == expected`
- `function_name(boundary) == expected`
- `function_name(invalid) raises error`
```

## Project Conventions

Adapt this section to your project:

- **Language:** (your language here)
- **Test framework:** (your framework here)
- **Spec location:** `specs/` directory or embedded in this file
- **Naming:** follow the target language's conventions

## Function Specifications

Add your RUNE specs below as Markdown sections, or reference `.rune` files:

<!-- Example:
### my_function

**SIGNATURE:** `def my_function(x: int) -> str`

**INTENT:** Describe what it does.

**BEHAVIOR:**
- WHEN x < 0 THEN raise error "x cannot be negative"
- OTHERWISE return str(x)

**TESTS:**
- `my_function(42) == "42"`
- `my_function(0) == "0"`
- `my_function(-1) raises error`
-->
