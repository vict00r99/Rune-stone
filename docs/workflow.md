# RUNE Workflow: From Requirements to Code

Two roles, two steps, one contract.

```
┌──────────────────────────┐     ┌──────────────────────────┐
│       ANALYST / PM       │     │       DEVELOPER          │
│                          │     │                          │
│  1. Write requirements   │     │  4. Generate code        │
│  2. Generate RUNE specs  │────▶│  5. Generate tests       │
│  3. Validate & refine    │     │  6. Audit over time      │
│                          │     │                          │
└──────────────────────────┘     └──────────────────────────┘
```

---

## Setup (once, 15 minutes)

Load the skills you need into your AI tool:

| Skill | File | Role |
|-------|------|------|
| **Writer** (required) | `skills/rune-writer.md` | Creates specs and implements code |
| Validator | `skills/rune-validator.md` | Checks spec completeness |
| Refiner | `skills/rune-refiner.md` | Suggests improvements |
| Test Generator | `skills/rune-test-generator.md` | Generates runnable test files |
| Diff | `skills/rune-diff.md` | Audits spec vs code drift |
| From Code | `skills/rune-from-code.md` | Reverse-engineers specs from existing code |
| Multi-Lang | `skills/rune-multi-lang.md` | Generates code in multiple languages |

**Start with just the Writer.** Add others as your workflow matures.

| Tool | How to load skills |
|------|-------------------|
| Claude Code | Copy to `.claude/skills/` |
| Claude Projects | Upload to Project Knowledge |
| Cursor | Copy to `.cursorrules` |
| Windsurf | Copy to `.windsurfrules` |
| Aider | `aider --read skills/rune-writer.md` |
| Any tool | Paste content into conversation |

For detailed setup per tool, see [Using Skills with AI Tools](using-skills-with-other-tools.md).

---

## Team Onboarding

### Who does what

| Role | Responsibility |
|------|---------------|
| **Tech lead** | Sets up skills, chooses format, decides where specs live |
| **Analyst / PM** | Writes requirements, generates and refines specs |
| **Developer** | Implements code from specs, generates tests, audits drift |

One person can fill all roles. The value is in having a spec, not in who writes it.

### First week

**Day 1 — Tech lead: set up and decide format**

1. Load the Writer skill into the team's AI tool
2. Choose a format:

| Use `.rune` files when... | Use Markdown sections when... |
|--------------------------|------------------------------|
| You want formal, parseable specs | You already use AGENTS.md |
| Specs live in a dedicated `specs/` directory | Specs live alongside project docs |
| Many functions to specify | A handful of key functions |
| You want to use the Validator skill | You want zero extra files |

Both formats follow the same pattern. You can mix both in the same project.

3. Optionally, copy [`AGENTS.md`](../AGENTS.md) from Runestone into your project as a reference

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

**Option A: Dedicated `specs/` directory**

```
my-project/
├── AGENTS.md              ← project context + skill references
├── specs/
│   ├── calculate_order_total.rune
│   ├── validate_coupon.rune
│   └── check_free_shipping.rune
├── src/
│   └── ...
└── tests/
    └── ...
```

**Option B: Specs inside AGENTS.md**

```
my-project/
├── AGENTS.md              ← project context + RUNE specs as Markdown sections
├── src/
│   └── ...
└── tests/
    └── ...
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

### Step 2: Generate a RUNE spec

**Skill: Writer**

For a Markdown spec:
```
Generate a RUNE spec from this requirement. Use markdown format.
```

For a standalone YAML file:
```
Generate a .rune file from this requirement.
```

### Step 3: Validate the spec

**Skill: Validator**

```
Validate this RUNE spec. Check all rules.
```

The Validator checks structure (required fields), content (WHEN/THEN format, test count), and consistency (every BEHAVIOR rule has a test).

### Step 4: Refine the spec

**Skill: Refiner**

```
Refine this RUNE spec. Find gaps and suggest improvements.
```

The Refiner identifies missing edge cases, weak test coverage, ambiguous rules, and incomplete constraints. Each suggestion includes ready-to-paste content.

### Step 5: Hand off

Save the spec and hand it to the developer. This is the contract.

---

## Part 2: Developer implements from specs

### Step 1: Generate implementation

**Skill: Writer**

From a `.rune` file:
```
Implement validate_coupon.rune. Follow the spec exactly.
```

From a markdown spec:
```
Implement the validate_coupon spec from AGENTS.md.
```

### Step 2: Generate tests

**Skill: Test Generator**

```
Generate tests from the validate_coupon spec.
```

The Test Generator creates a complete, runnable test file with concrete fixtures (expanding `[...]` from the spec), proper assertions, and framework-specific structure.

### Step 3: Run and verify

```bash
# Run tests with your framework
pytest tests/test_coupon.py -v
```

If tests fail, fix the code — not the spec (unless the spec has a genuine error).

### Step 4: Audit over time

**Skill: Diff**

After code changes, verify the implementation still matches the spec:

```
Compare validate_coupon.rune against src/coupon.py. Report any drift.
```

The Diff skill reports mismatches in signature, behavior, error messages, and undocumented behavior.

---

## Adopting RUNE on Existing Code

**Skill: From Code**

You don't need to start from requirements. Reverse-engineer specs from existing functions:

```
Generate a RUNE spec from this existing function: [paste code]
```

Then validate and refine the generated spec. From that point on, the spec is the source of truth.

---

## Multi-Language Projects

**Skill: Multi-Lang**

Generate implementations in multiple languages from one spec:

```
Implement slugify.rune in Python and TypeScript.
```

All implementations produce identical behavior. Error messages are the same across languages.

---

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        NEW FUNCTION                             │
│                                                                 │
│  Requirements ──▶ Writer ──▶ Validator ──▶ Refiner              │
│                                              │                  │
│                                              ▼                  │
│                          Writer (implement) + Test Generator    │
│                                              │                  │
│                                              ▼                  │
│                                    Code + Tests ──▶ Diff        │
│                                                   (ongoing)     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      EXISTING FUNCTION                          │
│                                                                 │
│  Existing code ──▶ From Code ──▶ Validator ──▶ Refiner ──▶ done │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     MULTI-LANGUAGE                               │
│                                                                 │
│  Spec (language: any) ──▶ Multi-Lang ──▶ N implementations      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prompt Reference

### For analysts

| Goal | Skill | Prompt |
|------|-------|--------|
| Generate spec | Writer | *"Generate a RUNE spec from this requirement: [description]"* |
| Choose format | Writer | Add: *"Use markdown format"* or *"Create a .rune file"* |
| Validate spec | Validator | *"Validate this RUNE spec"* |
| Improve spec | Refiner | *"Refine this RUNE spec. Find gaps."* |
| Spec from code | From Code | *"Create a RUNE spec from this function: [paste code]"* |

### For developers

| Goal | Skill | Prompt |
|------|-------|--------|
| Implement spec | Writer | *"Implement validate_coupon.rune"* |
| Generate tests | Test Generator | *"Generate tests from this spec"* |
| Multiple languages | Multi-Lang | *"Implement slugify.rune in Python and Go"* |
| Audit drift | Diff | *"Compare this spec against this code"* |

---

## Templates

The [`templates/`](../templates/) directory contains starter templates for writing specs manually:

- `basic-function.rune` — Standard synchronous function
- `async-function.rune` — Async/await function with timeout handling
- `class-spec.rune` — Class with multiple methods
- `agent-tool.rune` — Tool for an agent system
- `mcp-tool.rune` — MCP server tool

**You don't need templates if you use AI to generate specs.** The Writer skill already teaches the AI the complete pattern.

---

## Full Examples

- [Full pipeline](../examples/full-project/) — Requirements to specs to code
- [RUNE inside AGENTS.md](../examples/integrations/agents-md-with-rune/) — Markdown format embedded in AGENTS.md
- [Multi-language](../examples/multi-language/) — Same spec in Python + TypeScript

## FAQ

**Can the analyst and developer be the same person?**
Yes. The value is in having a spec to reference, not in who writes it.

**What if requirements change?**
Update the spec first, then regenerate the implementation.

**Do I need to install anything?**
No. Your existing AI tools are the runtime.

**Do I need all 7 skills?**
No. Start with the Writer. Add others as needed.

**Can I mix `.rune` files and markdown specs in the same project?**
Yes. Use whatever fits each function.

**How do specs fit into code review?**
Treat them like code. Include specs in pull requests. The spec is the source of truth.
