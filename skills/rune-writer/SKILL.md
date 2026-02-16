---
name: rune-writer
description: Create RUNE specifications from requirements and implement code from specs. Use when a user wants a RUNE spec (YAML or Markdown) or needs to implement code from an existing spec.
license: MIT
---

For the full RUNE pattern reference, see [SPEC.md](../../SPEC.md).

---

## The Pattern

Every RUNE spec defines these fields:

| Field | Required | Purpose |
|-------|----------|---------|
| SIGNATURE | Yes | Exact function interface in target language syntax |
| INTENT | Yes | What it does, 1-3 sentences |
| BEHAVIOR | Yes | Logic rules in WHEN/THEN format |
| TESTS | Yes | Minimum 3: happy path, boundary, error |
| CONSTRAINTS | No | Input validation rules |
| EDGE_CASES | No | Boundary conditions and expected behavior |
| DEPENDENCIES | No | External libraries |
| EXAMPLES | No | Usage examples |
| COMPLEXITY | No | Big-O time/space |

### Rules

- SIGNATURE must use the target language's actual syntax, not pseudocode
- BEHAVIOR must use WHEN/THEN format — each business rule = one clause
- TESTS must have at least 3 cases: one happy path, one boundary, one error
- INTENT must be 1-3 sentences, clear enough for a docstring
- Every BEHAVIOR rule must have at least one corresponding test
- Error messages in BEHAVIOR must be specific, not generic

---

## Format: YAML (.rune files)

Use standalone `.rune` files when you want formal, parseable specs. The SIGNATURE uses the target language's real syntax:

```yaml
---
meta:
  name: validate_coupon
  language: python
  version: 1.0
  tags: [e-commerce, validation]
---

RUNE: validate_coupon

SIGNATURE: |
  def validate_coupon(code: str, coupons: list[dict], current_date: str) -> tuple[bool, str]

INTENT: |
  Validates a coupon code against active coupons. Checks existence,
  expiration, and discount value. Case-insensitive matching.

BEHAVIOR:
  - WHEN code is empty THEN return (False, "Coupon code cannot be empty")
  - WHEN code not found (case-insensitive) THEN return (False, "Coupon code not found")
  - WHEN coupon has expired THEN return (False, "Coupon has expired")
  - OTHERWISE return (True, matching_coupon)

TESTS:
  - "validate_coupon('SAVE10', [...], '2025-01-15')[0] == True"
  - "validate_coupon('save10', [...], '2025-01-15')[0] == True"
  - "validate_coupon('INVALID', [...], '2025-01-15')[0] == False"
  - "validate_coupon('', [], '2025-01-15')[0] == False"
```

The pattern is the same in every language. Only the SIGNATURE syntax and naming conventions change.

## Format: Markdown (embedded in any .md)

Use markdown sections when embedding specs inside AGENTS.md or other docs:

```markdown
### validate_coupon

**SIGNATURE:** `def validate_coupon(code: str, coupons: list[dict], current_date: str) -> tuple[bool, str]`

**INTENT:** Validates a coupon code against active coupons. Checks existence, expiration, and discount value. Case-insensitive matching.

**BEHAVIOR:**
- WHEN code is empty THEN return (False, "Coupon code cannot be empty")
- WHEN code not found (case-insensitive) THEN return (False, "Coupon code not found")
- WHEN coupon has expired THEN return (False, "Coupon has expired")
- OTHERWISE return (True, matching_coupon)

**TESTS:**
- `validate_coupon('SAVE10', [...], '2025-01-15')[0] == True`
- `validate_coupon('', [], '2025-01-15')[0] == False`
```

Both formats contain the same information. The AI treats them identically.

---

## Generating Specs from Requirements

When a user describes what they need in plain language, generate a RUNE spec.

### Process

1. **Extract from the requirement:**
   - What is the function's purpose?
   - What are the inputs and outputs?
   - What are the business rules?
   - What could go wrong? (edge cases)

2. **Map each business rule to a WHEN/THEN clause** in BEHAVIOR

3. **Derive CONSTRAINTS** from input descriptions ("must be positive", "between 0 and 100")

4. **Derive EDGE_CASES** from boundaries (empty input, zero, max value, invalid types)

5. **Write TESTS** that verify each BEHAVIOR rule plus edge cases. Minimum 3, aim for 8-15.

6. **Ask the user** which format they want (YAML .rune file or Markdown section). If unclear, default to the same format used elsewhere in their project.

7. **Validate the spec** against the checklist below before presenting it.

---

## Validating Specs

When asked to validate a spec, or before presenting one you generated, check:

### Structure
- [ ] All required fields present: SIGNATURE, INTENT, BEHAVIOR, TESTS
- [ ] If YAML: valid YAML syntax, meta section with name and language
- [ ] If Markdown: headers use bold field names, code in backticks

### Content
- [ ] SIGNATURE uses actual language syntax (not pseudocode)
- [ ] BEHAVIOR uses WHEN/THEN format
- [ ] TESTS has at least 3 cases (happy path, boundary, error)
- [ ] INTENT is 1-3 sentences
- [ ] Every BEHAVIOR rule has at least one test
- [ ] Every EDGE_CASE has a corresponding test
- [ ] Error messages are specific (not generic "invalid input")

---

## Implementing from Specs

When given a RUNE spec (in either format) to implement, generate code that follows it exactly.

### Process

1. **Use the exact SIGNATURE** — function name, parameters, types, return type
2. **Implement each BEHAVIOR rule** in order — each WHEN/THEN becomes a conditional branch in the target language
3. **Add input validation** from CONSTRAINTS
4. **Handle every EDGE_CASE**
5. **Add a doc comment** from INTENT (docstring, JSDoc, GoDoc, rustdoc, etc.)
6. **Generate tests** from TESTS using the target language's testing framework

### Rules

- Never deviate from the SIGNATURE
- Implement ALL BEHAVIOR rules, not just some
- Every item in TESTS must have a corresponding test function
- Error messages must match those specified in BEHAVIOR
- Follow the target language's conventions
