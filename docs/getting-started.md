# Getting Started with RUNE

RUNE is a specification pattern that acts as a contract between what you want and what AI generates. It works in two formats: YAML files or Markdown sections.

## 5-Minute Quick Start

### 1. Load the skill

Upload [`skills/rune-writer.md`](../skills/rune-writer.md) to your AI tool. This teaches the AI the RUNE pattern.

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
- WHEN name is empty THEN raise ValueError("Name cannot be empty")
- WHEN formal is True THEN return "Good day, {name}."
- OTHERWISE return "Hey {name}!"

**TESTS:**
- `greet('Alice') == 'Hey Alice!'`
- `greet('Bob', formal=True) == 'Good day, Bob.'`
- `greet('') raises ValueError`

**EDGE_CASES:**
- Name with spaces: works correctly
- Name with special characters: works correctly
```

### 4. Implement from the spec

Tell the AI:

> "Implement the greet spec in Python"

You get:

```python
def greet(name: str, formal: bool = False) -> str:
    """Generates a greeting message. Formal or informal based on parameter."""
    if not name:
        raise ValueError("Name cannot be empty")
    if formal:
        return f"Good day, {name}."
    return f"Hey {name}!"
```

Plus tests:

```python
def test_informal():
    assert greet('Alice') == 'Hey Alice!'

def test_formal():
    assert greet('Bob', formal=True) == 'Good day, Bob.'

def test_empty_name():
    with pytest.raises(ValueError):
        greet('')
```

That's it. The spec is the contract. The AI follows it.

## Two Formats, Same Pattern

**As a Markdown section** (embed in AGENTS.md or any doc):
```markdown
### greet
**SIGNATURE:** `def greet(name: str, formal: bool = False) -> str`
**BEHAVIOR:**
- WHEN name is empty THEN raise ValueError
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
  - WHEN name is empty THEN raise ValueError
  - WHEN formal is True THEN return "Good day, {name}."
  - OTHERWISE return "Hey {name}!"
TESTS:
  - "greet('Alice') == 'Hey Alice!'"
```

Both produce the same implementation. Use whichever fits your workflow.

## Next Steps

- **[Workflow Guide](workflow.md)** — Complete guide for analysts and developers
- **[Full Pipeline Example](../examples/full-project/)** — Requirements to specs to code
- **[Before & After](before-after.md)** — See the difference RUNE makes
- **[SPEC.md](../SPEC.md)** — Full pattern reference
- **[Templates](../templates/)** — Starter templates
