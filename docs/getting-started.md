# Getting Started with RUNE

RUNE is a specification pattern that acts as a contract between what you want and what AI generates. It works in two formats: YAML files or Markdown sections. It works with any programming language.

## 5-Minute Quick Start

### 1. Load the skill

Upload [`skills/rune-writer.md`](../skills/rune-writer.md) to your AI tool. This teaches the AI the RUNE pattern.

| Tool | How to load |
|------|------------|
| Claude Code | Copy to `.claude/skills/` |
| Claude Projects | Upload to Project Knowledge |
| Cursor | Copy to `.cursorrules` |
| Aider | `aider --read skills/rune-writer.md` |
| Any tool | Paste content into conversation |

For detailed setup per tool, see [Using Skills with AI Tools](using-skills-with-other-tools.md).

### 2. Describe what you need

Tell the AI:

> "I need a function that greets someone by name. Formal mode says 'Good day, Name.' Informal mode says 'Hey Name!' Empty name should raise an error. Generate a RUNE spec."

### 3. Get a spec

The AI generates:

```markdown
### greet

**SIGNATURE:** `def greet(name: str, formal: bool = False) -> str`

**INTENT:** Generates a greeting message. Formal or informal based on parameter.

**BEHAVIOR:**
- WHEN name is empty THEN raise error "Name cannot be empty"
- WHEN formal is True THEN return "Good day, {name}."
- OTHERWISE return "Hey {name}!"

**TESTS:**
- `greet('Alice') == 'Hey Alice!'`
- `greet('Bob', formal=True) == 'Good day, Bob.'`
- `greet('') raises error`

**EDGE_CASES:**
- Name with spaces: works correctly
- Name with special characters: works correctly
```

### 4. Implement from the spec

Tell the AI:

> "Implement the greet spec in Python"

Or in any other language:

> "Implement the greet spec in Go"

The AI generates code + tests that follow the spec exactly.

---

## Two Formats, Same Pattern

**As a Markdown section** (embed in AGENTS.md or any doc):
```markdown
### greet
**SIGNATURE:** `def greet(name: str, formal: bool = False) -> str`
**BEHAVIOR:**
- WHEN name is empty THEN raise error "Name cannot be empty"
- WHEN formal is True THEN return "Good day, {name}."
- OTHERWISE return "Hey {name}!"
**TESTS:**
- `greet('Alice') == 'Hey Alice!'`
```

**As a `.rune` file** (standalone YAML):
```yaml
---
meta:
  name: greet
  language: python
---
RUNE: greet
SIGNATURE: |
  def greet(name: str, formal: bool = False) -> str
BEHAVIOR:
  - WHEN name is empty THEN raise error "Name cannot be empty"
  - WHEN formal is True THEN return "Good day, {name}."
  - OTHERWISE return "Hey {name}!"
TESTS:
  - "greet('Alice') == 'Hey Alice!'"
```

Both produce code with the same behavior. Use whichever fits your workflow.

---

## Skills Overview

Runestone provides 7 skills. The writer is enough to start. Add others as your workflow grows.

```
Requirements ──▶ Writer ──▶ Validator ──▶ Refiner ──▶ Writer (implement) + Test Generator
                                                              │
                                                              ▼
                                                           Diff (audit over time)
```

| Skill | File | What it does |
|-------|------|-------------|
| **Writer** | [`rune-writer.md`](../skills/rune-writer.md) | Create specs and implement code from them |
| **Validator** | [`rune-validator.md`](../skills/rune-validator.md) | Check if a spec is complete and well-formed |
| **Refiner** | [`rune-refiner.md`](../skills/rune-refiner.md) | Suggest missing tests, edge cases, and clarifications |
| **Test Generator** | [`rune-test-generator.md`](../skills/rune-test-generator.md) | Generate runnable test files from a spec |
| **Diff** | [`rune-diff.md`](../skills/rune-diff.md) | Compare spec vs implementation to detect drift |
| **From Code** | [`rune-from-code.md`](../skills/rune-from-code.md) | Reverse-engineer a spec from existing code |
| **Multi-Lang** | [`rune-multi-lang.md`](../skills/rune-multi-lang.md) | Generate implementations in multiple languages from one spec |

**Start with just the Writer.** Add Validator and Test Generator when you want more rigor. Add the rest as needed.

---

## Adopting RUNE on Existing Code

You don't have to start from scratch. Use the **From Code** skill:

> "Here's my existing function. Generate a RUNE spec that describes its current behavior."

Then validate and refine the generated spec. From that point on, the spec is the source of truth.

---

## Using AGENTS.md

Copy [`AGENTS.md`](../AGENTS.md) from the Runestone project root into your own project. It contains:
- Context about the RUNE pattern
- References to all skills
- The workflow diagram
- A section where you can add your own specs as Markdown sections

This gives any AI tool working in your project immediate context about how to create and use RUNE specs.

---

## Next Steps

- **[Workflow Guide](workflow.md)** — Complete guide for analysts and developers
- **[Full Pipeline Example](../examples/full-project/)** — Requirements to specs to code
- **[Before & After](before-after.md)** — See the difference RUNE makes
- **[SPEC.md](../SPEC.md)** — Full pattern reference
- **[Templates](../templates/)** — Starter templates for manual writing
