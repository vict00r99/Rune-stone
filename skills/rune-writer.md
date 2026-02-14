# RUNE Skill

Upload this file to any AI tool (Claude Projects, Cursor, Aider, ChatGPT, Copilot) to enable RUNE specification workflows.

---

## What is RUNE

RUNE is a specification pattern for defining function behavior before implementation. It ensures any AI coding tool generates code with consistent behavior from the same contract. Internal details (variable names, code style) may vary, but the function's inputs, outputs, and edge case handling remain the same.

RUNE is a pattern, not a file format. The same structure can be written in:
- **YAML** as standalone `.rune` files (formal, parseable)
- **Markdown** as sections inside AGENTS.md, README.md, or any .md file

The value is in the structure (WHEN/THEN rules, mandatory tests, explicit edge cases), not in the container. Both formats produce code with the same behavior.

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

**Python example:**
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

**Go example:**
```yaml
---
meta:
  name: CalculateDiscount
  language: go
  version: 1.0
---

RUNE: CalculateDiscount

SIGNATURE: |
  func CalculateDiscount(price float64, percentage int) (float64, error)

INTENT: |
  Calculates the final price after applying a discount percentage.
  Returns the discounted price rounded to 2 decimal places.

BEHAVIOR:
  - WHEN percentage < 0 THEN return error "Discount percentage cannot be negative"
  - WHEN percentage > 100 THEN return error "Discount percentage cannot exceed 100"
  - WHEN price < 0 THEN return error "Price cannot be negative"
  - CALCULATE final_price = price - (price * percentage / 100), round to 2 decimals
  - RETURN final_price

TESTS:
  - "CalculateDiscount(100.0, 20) == 80.0"
  - "CalculateDiscount(100.0, 0) == 100.0"
  - "CalculateDiscount(-10.0, 20) returns error"
```

**TypeScript example:**
```yaml
---
meta:
  name: calculateDiscount
  language: typescript
  version: 1.0
---

RUNE: calculateDiscount

SIGNATURE: |
  function calculateDiscount(price: number, percentage: number): number

BEHAVIOR:
  - WHEN percentage < 0 THEN throw "Discount percentage cannot be negative"
  - WHEN percentage > 100 THEN throw "Discount percentage cannot exceed 100"
  - WHEN price < 0 THEN throw "Price cannot be negative"
  - RETURN price - (price * percentage / 100), rounded to 2 decimals

TESTS:
  - "calculateDiscount(100.0, 20) === 80.0"
  - "calculateDiscount(100.0, 0) === 100.0"
  - "calculateDiscount(-10.0, 20) throws"
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
