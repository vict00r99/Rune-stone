# RUNE Workflow: From Requirements to Code

Two roles, two steps, one contract.

```
┌──────────────────────────┐     ┌──────────────────────────┐
│       ANALYST / PM       │     │       DEVELOPER          │
│                          │     │                          │
│  1. Write requirements   │     │  3. Generate code        │
│  2. Generate RUNE specs  │────▶│  4. Generate tests       │
│                          │     │                          │
└──────────────────────────┘     └──────────────────────────┘
```

---

## Setup (once, 15 minutes)

Upload **one file** to your AI tool: [`skills/rune-writer.md`](../skills/rune-writer.md)

This single file teaches the AI everything about the RUNE pattern — how to generate specs from requirements, validate them, and implement code from them.

| Tool | How to load |
|------|------------|
| Claude Projects | Upload to Project Knowledge |
| Cursor | Copy to `.cursorrules` |
| Windsurf | Copy to `.windsurfrules` |
| Aider | `aider --read skills/rune-writer.md` |
| ChatGPT | Paste content into conversation |
| Copilot Chat | `#file:skills/rune-writer.md` |

For detailed setup per tool, see [Using Skills with AI Tools](using-skills-with-other-tools.md).

---

## Team Onboarding

### Who does what

| Role | Responsibility | Reference |
|------|---------------|-----------|
| **Tech lead** | Sets up the AI tool, chooses format, decides where specs live | This section |
| **Analyst / PM** | Writes requirements, generates RUNE specs with AI | [Part 1](#part-1-analyst-generates-specs) |
| **Developer** | Implements code from specs, runs tests | [Part 2](#part-2-developer-implements-from-specs) |

One person can fill all roles. The value is in having a spec, not in who writes it.

### First week

**Day 1 — Tech lead: set up and decide format**

1. Upload `skills/rune-writer.md` to the team's AI tool (see [setup table above](#setup-once-15-minutes))
2. Choose a format:

| Use `.rune` files when... | Use Markdown sections when... |
|--------------------------|------------------------------|
| You want formal, parseable specs | You already use AGENTS.md |
| Specs live in a dedicated `specs/` directory | Specs live alongside project docs |
| Many functions to specify | A handful of key functions |
| You want to use the validator tool | You want zero extra files |

Both formats follow the same pattern. The AI treats them identically. You can mix both in the same project.

3. Decide where specs live in the repo (see [project structure](#project-structure) below)

**Day 2 — Analyst: write the first spec**

Pick one real function the team needs. Follow [Part 1](#part-1-analyst-generates-specs). The first spec teaches the pattern faster than any documentation.

**Day 3 — Developer: implement from the spec**

Take the spec from Day 2. Follow [Part 2](#part-2-developer-implements-from-specs). Run the tests. If all pass, the team has adopted RUNE.

**Ongoing — treat specs like code**

- Review specs in pull requests, just like code
- Update the spec first when requirements change, then regenerate
- New function? Spec first, implement second

### Project structure

Organize specs however fits your project. Two common patterns:

**Option A: Dedicated `specs/` directory** (for teams with many specs)

```
my-project/
├── specs/
│   ├── calculate_order_total.rune
│   ├── validate_coupon.rune
│   └── check_free_shipping.rune
├── src/
│   ├── order_total.py
│   ├── coupon.py
│   └── shipping.py
└── tests/
    ├── test_order_total.py
    ├── test_coupon.py
    └── test_shipping.py
```

**Option B: Specs inside AGENTS.md** (for teams already using AGENTS.md)

```
my-project/
├── AGENTS.md          ← contains project context + RUNE specs
├── src/
│   ├── order_total.py
│   ├── coupon.py
│   └── shipping.py
└── tests/
```

See [RUNE inside AGENTS.md](../examples/integrations/agents-md-with-rune/) for a complete example.

---

## Part 1: Analyst generates specs

### Step 1: Describe requirements in plain language

```
I need a function that validates coupon codes at checkout.

Rules:
- Receives a coupon code and checks it against active coupons
- Codes are case-insensitive (SAVE10 = save10)
- Must check if the coupon has expired
- Returns whether it's valid plus the coupon data or error message
```

### Step 2: Ask the AI to generate a RUNE spec

For a Markdown spec:
```
Generate a RUNE spec from this requirement. Use markdown format.
```

For a standalone YAML file:
```
Generate a .rune file from this requirement. Target language: Python.
```

### Step 3: Review and iterate

Check the generated spec:
- Does the BEHAVIOR cover all your rules?
- Are the TESTS complete? (minimum 3: happy, boundary, error)
- Are the EDGE_CASES reasonable?

If something's wrong:
```
Add an edge case for when the coupons list is empty.
Change the return type to tuple[bool, dict | str].
```

### Step 4: Hand off

Save the spec (as `.rune` file or markdown section) and hand it to the developer. This is the contract.

---

## Part 2: Developer implements from specs

### Step 1: Generate implementation

From a `.rune` file:
```
Implement validate_coupon.rune in Python. Follow the spec exactly.
```

From a markdown spec:
```
Implement the validate_coupon spec from AGENTS.md.
```

### Step 2: Generate tests

```
Generate pytest tests from the validate_coupon spec.
```

### Step 3: Run and verify

```bash
pytest tests/test_coupon.py -v
```

If tests fail, fix the code — not the spec (unless the spec has a genuine error).

---

## Prompt Reference

### For analysts

| Goal | Prompt |
|------|--------|
| Generate spec from requirements | *"Generate a RUNE spec from this requirement: [description]"* |
| Choose format | Add: *"Use markdown format"* or *"Create a .rune file"* |
| Iterate | *"Add an edge case for empty input. Change the return type."* |
| Spec from existing code | *"Create a RUNE spec that describes this function: [paste code]"* |

### For developers

| Goal | Prompt |
|------|--------|
| Implement a spec | *"Implement validate_coupon.rune in Python"* |
| Generate tests | *"Generate pytest tests from this spec"* |
| Another language | *"Implement slugify.rune in TypeScript"* |
| Check compliance | *"Does this code match the spec? [paste code]"* |

---

## Templates

The [`templates/`](../templates/) directory contains starter templates for writing specs manually:

- `basic-function.rune` — Standard synchronous function
- `async-function.rune` — Async/await function with timeout handling
- `class-spec.rune` — Class with multiple methods
- `agent-tool.rune` — Tool for an agent system
- `mcp-tool.rune` — MCP server tool

**You don't need templates if you use AI to generate specs.** The skill file (`rune-writer.md`) already teaches the AI the complete pattern. Templates are useful if you prefer writing specs by hand or want to see the YAML structure as reference.

---

## Full Examples

- [Full pipeline](../examples/full-project/) — Requirements to specs to code (start here)
- [RUNE inside AGENTS.md](../examples/integrations/agents-md-with-rune/) — Markdown format embedded in AGENTS.md
- [Multi-language](../examples/multi-language/) — Same spec in Python + TypeScript

## FAQ

**Can the analyst and developer be the same person?**
Yes. The value is in having a spec to reference, not in who writes it.

**What if requirements change?**
Update the spec first, then regenerate the implementation.

**Do I need to install anything?**
No. Your existing AI tools are the runtime. Optionally use `python tools/validate.py` for YAML spec validation.

**Do I need templates to start?**
No. Tell the AI your requirements and it generates a complete spec. Templates are optional reference material for manual writing.

**Can I mix `.rune` files and markdown specs in the same project?**
Yes. Use `.rune` files for functions that need formal, standalone specs and markdown sections for functions documented alongside project context in AGENTS.md.

**How do specs fit into code review?**
Treat them like code. Include specs in pull requests. Review the BEHAVIOR and TESTS before approving. The spec is the source of truth — if the code doesn't match the spec, fix the code.
