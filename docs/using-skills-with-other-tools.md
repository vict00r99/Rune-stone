# Using RUNE with AI Coding Tools

This guide shows how to configure popular AI coding assistants to use the RUNE pattern, so they know how to generate specs (in YAML or Markdown), validate them, and implement code from them.

## Overview

The RUNE skill lives in `skills/rune-writer.md`. This single file teaches any AI assistant the complete RUNE pattern — both formats (YAML `.rune` files and Markdown sections), spec generation, validation, and implementation. Each tool has its own way of loading it.

| Tool | Method | Auto-loads? |
|------|--------|-------------|
| Claude Code | `.claude/skills/` directory | Yes |
| Claude Projects | Project Knowledge upload | Yes |
| Cursor | `.cursorrules` file | Yes |
| Windsurf | `.windsurfrules` file | Yes |
| Aider | `--read` flag or `.aider.conf.yml` | Manual |
| Continue.dev | `.continuerc.json` config | Yes |
| GitHub Copilot Chat | `#file` reference | Manual |
| ChatGPT / Generic | Paste into system prompt | Manual |

---

## Claude Code

Claude Code automatically loads skill files from `.claude/skills/` at startup.

### Setup

Copy the skill file into your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills
cp skills/rune-writer.md .claude/skills/runestone-skills.md
```

### Verify

```bash
cd runestone
claude

# Skills are loaded -- try it
> Create a RUNE spec for a temperature converter
```

### Keeping in Sync

If you update `skills/rune-writer.md`, re-copy it:

```bash
cp skills/rune-writer.md .claude/skills/runestone-skills.md
```

---

## Claude Projects

Claude Projects let you upload files as persistent knowledge across conversations.

### Setup

1. Open [claude.ai](https://claude.ai) and create or open a project
2. Go to **Project Knowledge**
3. Click **Add content** and upload:
   - `skills/rune-writer.md` (the RUNE pattern)
   - Any `.rune` files or docs containing markdown specs you want Claude to reference
4. Add to **Project Instructions**:

```markdown
When working with RUNE specifications:
1. Follow the RUNE pattern defined in rune-writer.md
2. Specs can be written as YAML (.rune files) or Markdown sections
3. Always validate specs against the checklist before finalizing

When implementing from a RUNE spec (either format):
1. Read the entire spec carefully
2. Follow SIGNATURE exactly
3. Implement all BEHAVIOR rules
4. Handle all EDGE_CASES
5. Include all TESTS
6. Add docstring from INTENT
```

### Usage

```
User: Create a RUNE spec for a URL shortener (use markdown format)
Claude: [Uses rune-writer.md to create a Markdown spec]

User: Create a .rune file for a URL shortener
Claude: [Uses rune-writer.md to create a YAML spec]

User: Implement the URL shortener spec
Claude: [Reads spec, generates implementation with tests]
```

### FAQ

**Should I upload all specs at once?**
Start with core specs, add more as needed. Claude handles dozens of specs fine, but organize them logically.

**How do I keep specs and code in sync?**
Always update the spec first, then regenerate implementation. The spec is the source of truth.

**Can Claude create specs from existing code?**
Yes -- ask: "Create a RUNE spec from this existing function: [paste code]"

For a complete Claude Projects example, see [`examples/integrations/claude-project-example/`](../examples/integrations/claude-project-example/).

---

## Cursor

Cursor reads project-level instructions from `.cursorrules` at the project root.

### Setup (Option A: Dedicated File)

Create `.cursorrules` in your project root:

```bash
cp skills/rune-writer.md .cursorrules
```

### Setup (Option B: Reference in Existing Rules)

If you already have a `.cursorrules` file, append a reference:

```markdown
# .cursorrules

## RUNE Specifications

This project uses the RUNE specification pattern for AI code generation.
Specs can be written as `.rune` YAML files or as Markdown sections in AGENTS.md.

When working with RUNE specs (either format):
- Read `skills/rune-writer.md` for the complete pattern reference
- Required fields: SIGNATURE, INTENT, BEHAVIOR, TESTS
- YAML `.rune` files also need: meta (name, language), RUNE header
- Use WHEN/THEN format in BEHAVIOR sections
- Include minimum 3 tests per spec (happy path, boundary, error)
- Write SIGNATURE in the target language's actual syntax
- Keep INTENT to 1-3 sentences

When asked to implement from a spec:
1. Read the spec completely
2. Match SIGNATURE exactly
3. Implement all BEHAVIOR rules
4. Handle all EDGE_CASES
5. Generate tests from TESTS section
6. Add docstring from INTENT
```

### Setup (Option C: Cursor Settings)

In Cursor, go to **Settings > Rules for AI** and paste the content of `skills/rune-writer.md`.

### Usage

```
# In Cursor chat (Cmd+K or Ctrl+K):
"Create a RUNE spec for input sanitization"
"Create a .rune file for input sanitization"
"Implement this spec"
"Validate this spec against RUNE standards"
```

---

## Windsurf

Windsurf uses `.windsurfrules` for project-level AI instructions.

### Setup

Create `.windsurfrules` in your project root:

```bash
cp skills/rune-writer.md .windsurfrules
```

Or add a condensed version:

```markdown
# .windsurfrules

## RUNE Specification Pattern

This project uses RUNE for AI code generation specs.
Pattern reference: SPEC.md | Skill: skills/rune-writer.md

Two formats:
- YAML (.rune files): standalone specs with meta header (name, language)
- Markdown sections: embedded in AGENTS.md or any .md file

Required fields (both formats): SIGNATURE, INTENT, BEHAVIOR, TESTS
Optional fields: CONSTRAINTS, EDGE_CASES, DEPENDENCIES, EXAMPLES, COMPLEXITY

Rules:
- SIGNATURE must use target language syntax (not pseudocode)
- BEHAVIOR must use WHEN/THEN format
- TESTS must have 3+ cases: happy path, boundary, error
- INTENT: 1-3 sentences max

When implementing from a spec, follow SIGNATURE exactly and implement
all BEHAVIOR rules. Generate tests from the TESTS section.
```

---

## Aider

Aider can load read-only context files that inform the AI without being edited.

### Setup (Option A: Command Line)

Pass the skill file with `--read`:

```bash
# Single session
aider --read skills/rune-writer.md src/my_module.py

# With a .rune spec for implementation
aider --read skills/rune-writer.md --read specs/validate_coupon.rune src/coupon.py

# With an AGENTS.md that contains markdown specs
aider --read skills/rune-writer.md --read AGENTS.md src/coupon.py
```

### Setup (Option B: Configuration File)

Create `.aider.conf.yml` in the project root:

```yaml
# .aider.conf.yml
read:
  - skills/rune-writer.md
```

Now every `aider` session in this project automatically loads the skill:

```bash
aider src/my_module.py
# Skill is loaded from .aider.conf.yml
```

### Usage

```bash
# Create a spec (markdown format)
aider --read skills/rune-writer.md docs/specs.md
> Create a RUNE spec for a markdown-to-HTML converter

# Create a spec (YAML format)
aider --read skills/rune-writer.md new_spec.rune
> Create a .rune file for a markdown-to-HTML converter

# Implement from spec
aider --read skills/rune-writer.md --read specs/my_spec.rune src/implementation.py
> Implement the function defined in my_spec.rune
```

---

## Continue.dev

Continue.dev (VS Code / JetBrains extension) supports custom context providers and system prompts.

### Setup

Add to `.continuerc.json` in your project root:

```json
{
  "systemMessage": "You are working on a project that uses the RUNE specification pattern. Specs can be written as YAML (.rune files) or as Markdown sections in AGENTS.md. Follow the pattern defined in skills/rune-writer.md. Required fields: SIGNATURE, INTENT, BEHAVIOR (WHEN/THEN format), TESTS (3+ cases). YAML files also need a meta header with name and language.",
  "docs": [
    {
      "title": "RUNE Skill",
      "startUrl": "skills/rune-writer.md"
    }
  ]
}
```

### Usage

In the Continue.dev chat panel, reference files with `@`:

```
@skills/rune-writer.md Create a RUNE spec for a rate limiter
@specs/validate_coupon.rune Implement this spec
@AGENTS.md Implement the validate_coupon spec from this file
```

---

## GitHub Copilot Chat

Copilot Chat in VS Code can reference files with the `#file` syntax.

### Setup

No configuration needed -- reference files directly in chat.

### Usage

```
#file:skills/rune-writer.md Create a RUNE spec for a JWT token validator

#file:skills/rune-writer.md #file:specs/validate_email.rune
Implement this spec following the RUNE pattern

#file:skills/rune-writer.md #file:AGENTS.md
Implement the validate_coupon spec from AGENTS.md
```

For persistent instructions, add to `.github/copilot-instructions.md`:

```markdown
# Copilot Instructions

## RUNE Specifications

This project uses the RUNE pattern for AI code generation.
Specs can be written as YAML (.rune files) or as Markdown sections in AGENTS.md.

When working with RUNE specs:
- Read `skills/rune-writer.md` for the complete pattern
- Required fields: SIGNATURE, INTENT, BEHAVIOR, TESTS
- YAML files also need: meta header (name, language)
- Use WHEN/THEN format in BEHAVIOR
- Include 3+ test cases per spec
- Write SIGNATURE in the target language's syntax
```

---

## ChatGPT / Generic AI Tools

For AI tools that don't support file-based configuration, paste the skill content directly.

### Setup

1. Open `skills/rune-writer.md` in a text editor
2. Copy the entire contents
3. Paste at the start of your AI conversation:

```
Here is the RUNE specification pattern. Follow it when I ask
you to create, validate, or implement specs:

[paste contents of skills/rune-writer.md]

---

Now let's work. Create a RUNE spec for a password strength checker.
```

### With Custom GPTs

If using OpenAI's custom GPTs:

1. Create a new GPT
2. In **Instructions**, paste the content of `skills/rune-writer.md`
3. In **Knowledge**, upload example `.rune` files or markdown specs
4. The GPT will always follow the RUNE pattern

---

## Validation

Regardless of which AI tool you use, you can validate YAML `.rune` files with the CLI validator:

```bash
# Validate a single spec
python tools/validate.py my_spec.rune

# Validate all specs in a directory
python tools/validate.py specs/

# Strict mode (checks optional fields)
python tools/validate.py --strict my_spec.rune

# JSON output for CI/CD
python tools/validate.py --json specs/ > validation-report.json
```

Note: The validator works with `.rune` YAML files. Markdown specs are validated by the AI during generation (the skill file includes a validation checklist).

---

## Comparison

| Feature | Claude Code | Claude Projects | Cursor | Aider | Copilot Chat |
|---------|------------|----------------|--------|-------|-------------|
| Auto-load skill | Yes | Yes | Yes | With config | No |
| Reference .rune files | Yes | Upload | Yes | `--read` | `#file` |
| Reference markdown specs | Yes | Upload | Yes | `--read` | `#file` |
| Run validator | Yes (bash) | No | Yes (terminal) | Yes (bash) | No |
| Generate from spec | Yes | Yes | Yes | Yes | Yes |

---

## Troubleshooting

### Skill not being followed

**Problem:** The AI ignores the RUNE pattern even after loading the skill.

**Solution:** Be explicit in your prompt:
```
Following the RUNE pattern from rune-writer.md, create a spec for...
```

### YAML syntax errors in generated specs

**Problem:** AI generates `.rune` files with invalid YAML.

**Solution:** Run the validator after generation:
```bash
python tools/validate.py generated_spec.rune
```
Then ask the AI to fix any reported errors.

### Tool doesn't support file references

**Problem:** Your AI tool can't load external files.

**Solution:** Paste a condensed version into your prompt:
```
RUNE specs define function contracts. Required fields: SIGNATURE (exact
function interface), INTENT (1-3 sentences), BEHAVIOR (WHEN/THEN rules),
TESTS (3+ cases: happy path, boundary, error). Optional: CONSTRAINTS,
EDGE_CASES, DEPENDENCIES, EXAMPLES, COMPLEXITY.
Specs can be YAML (.rune files) or Markdown sections.
```

### Skill file out of sync

**Problem:** `.claude/skills/runestone-skills.md` differs from `skills/rune-writer.md`.

**Solution:** The `skills/` directory is the source of truth. Copy it:
```bash
cp skills/rune-writer.md .claude/skills/runestone-skills.md
```

---

## Resources

- [RUNE Specification](../SPEC.md) -- Full pattern reference
- [Skill File](../skills/rune-writer.md) -- The one file that teaches the AI
- [Getting Started](getting-started.md) -- 5-minute tutorial
- [Workflow Guide](workflow.md) -- Team adoption and workflow
