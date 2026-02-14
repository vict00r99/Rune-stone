# RUNE Validator Skill

Validates RUNE specifications against the official pattern rules. Use this skill when you receive a `.rune` file or a Markdown spec section and need to check if it is complete, well-formed, and internally consistent.

---

## How to Use

When asked to **validate a RUNE spec**, run every check below and return a structured report.

Input: a `.rune` YAML file or a Markdown section following the RUNE pattern.

---

## Validation Checklist

### 1. Structure Checks

Run these checks first. If any fail, the spec is invalid.

| # | Rule | Pass condition |
|---|------|---------------|
| S1 | Required fields present | SIGNATURE, INTENT, BEHAVIOR, and TESTS all exist |
| S2 | YAML meta header (YAML only) | `meta.name` and `meta.language` are present |
| S3 | RUNE header matches meta.name (YAML only) | `RUNE:` value equals `meta.name` |
| S4 | Markdown formatting (Markdown only) | Field names are bold (`**SIGNATURE:**`), code in backticks |
| S5 | Valid YAML syntax (YAML only) | File parses without YAML errors |

### 2. Content Checks

| # | Rule | Pass condition |
|---|------|---------------|
| C1 | SIGNATURE uses real language syntax | Not pseudocode. Uses the target language's actual function declaration syntax |
| C2 | INTENT is 1-3 sentences | No more than 3 sentences. No implementation details (no algorithms, regex, library names) |
| C3 | BEHAVIOR uses WHEN/THEN format | Every rule is a WHEN/THEN clause, with an optional OTHERWISE as the last rule |
| C4 | BEHAVIOR rules are ordered correctly | Validations first, business logic second, default (OTHERWISE) last |
| C5 | TESTS has at least 3 cases | Minimum: 1 happy path, 1 boundary, 1 error case |
| C6 | TESTS use correct format | Each test is `function(input) == expected` or `function(input) raises ErrorType` |

### 3. Consistency Checks

| # | Rule | Pass condition |
|---|------|---------------|
| X1 | Every BEHAVIOR rule has a test | Each WHEN/THEN clause maps to at least one test case |
| X2 | Every EDGE_CASE has a test | If EDGE_CASES is present, each entry maps to a test |
| X3 | CONSTRAINTS have BEHAVIOR rules | Each constraint that requires runtime validation has a corresponding WHEN/THEN rule |
| X4 | Error messages match | Error messages in BEHAVIOR match the messages expected in TESTS |
| X5 | SIGNATURE matches TESTS | Function name and parameter count in TESTS match SIGNATURE |

---

## Output Format

Return the report in this format:

```markdown
## RUNE Validation Report: `<function_name>`

### Structure
- [PASS] S1: Required fields present
- [PASS] S2: YAML meta header valid
- [FAIL] S3: RUNE header mismatch — RUNE says "validate_email" but meta.name is "email_validator"

### Content
- [PASS] C1: SIGNATURE uses real language syntax
- [WARN] C2: INTENT has 4 sentences (max 3 recommended)
- [PASS] C3: BEHAVIOR uses WHEN/THEN format
...

### Consistency
- [FAIL] X1: BEHAVIOR rule "WHEN code is empty THEN ..." has no corresponding test
- [PASS] X2: All EDGE_CASES have tests
...

### Summary
- **Status:** FAIL (2 errors, 1 warning)
- **Errors:** S3, X1
- **Warnings:** C2
- **Suggestions:**
  - Rename RUNE header to match meta.name
  - Add test: `validate_email('') == (False, "Email cannot be empty")`
  - Consider shortening INTENT to 3 sentences
```

---

## Severity Levels

- **FAIL** — Spec violates a required rule. Must be fixed before implementation.
- **WARN** — Spec is technically valid but has a quality issue. Should be fixed.
- **PASS** — Rule satisfied.

---

## Rules

- Always run ALL checks, even if early checks fail
- Report every issue found, not just the first one
- For each FAIL or WARN, include a specific suggestion on how to fix it
- If the spec is valid (all PASS), say so clearly
- Do not modify the spec — only report findings
