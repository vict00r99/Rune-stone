# RUNE From Code Skill

Reverse-engineers a RUNE specification from an existing function or class. Use this skill to adopt the RUNE pattern in existing projects without rewriting code from scratch. Works with any programming language.

---

## How to Use

When given an existing function (or class method), analyze it and generate a complete RUNE spec that describes its current behavior.

Input: source code of one or more functions (any language).
Output: a `.rune` YAML spec or Markdown section for each function.

---

## Process

### Step 1: Extract SIGNATURE

Read the function declaration exactly as written. Use the source language's actual syntax:

**Python:**
```python
def calculate_discount(price: float, percentage: int) -> float:
```
```yaml
SIGNATURE: |
  def calculate_discount(price: float, percentage: int) -> float
```

**Go:**
```go
func CalculateDiscount(price float64, percentage int) (float64, error) {
```
```yaml
SIGNATURE: |
  func CalculateDiscount(price float64, percentage int) (float64, error)
```

**TypeScript:**
```typescript
function calculateDiscount(price: number, percentage: number): number {
```
```yaml
SIGNATURE: |
  function calculateDiscount(price: number, percentage: number): number
```

If the language doesn't have type annotations (plain JavaScript, Ruby, Lua), infer types from:
- Parameter names and usage within the function body
- Default values and return statements
- Add a comment noting the inference: `# types inferred from usage`

### Step 2: Write INTENT

Summarize what the function does in 1-3 sentences based on:
- The function name
- The docstring/doc comment (if present)
- The overall behavior

Do NOT describe implementation details. Describe purpose.

```yaml
# Bad (implementation details):
INTENT: |
  Uses regex pattern to match RFC 5322 emails and returns a tuple.

# Good (purpose):
INTENT: |
  Validates an email address against RFC 5322 standards.
  Returns a validity flag and a message explaining the result.
```

### Step 3: Extract BEHAVIOR Rules

Analyze the function's control flow and convert each branch to a WHEN/THEN rule. The source language varies, but the BEHAVIOR output is always the same WHEN/THEN format:

**From Python:**
```python
if not email:
    return (False, "Email cannot be empty")
```

**From Go:**
```go
if email == "" {
    return false, fmt.Errorf("email cannot be empty")
}
```

**From Rust:**
```rust
if email.is_empty() {
    return Err("Email cannot be empty".to_string());
}
```

**All extract to the same BEHAVIOR:**
```yaml
BEHAVIOR:
  - WHEN email is empty THEN return error "Email cannot be empty"
```

Rules for extraction:
- Each conditional branch that returns or raises/throws becomes a WHEN/THEN
- The final return or else branch becomes OTHERWISE
- Preserve the exact error messages from the code
- Preserve the order of checks (top to bottom)
- Collapse implementation details into business-level descriptions
- Map language-specific error mechanisms to neutral language:
  - Python `raise ValueError` / Go `return err` / Rust `Err()` / Java `throw` → "raise error" or "return error"

### Step 4: Extract CONSTRAINTS

Look for input validation patterns in any language:
- Type checks (type annotations, `instanceof`, `is`, type guards, pattern matching)
- Range checks (comparisons against bounds)
- Format checks (regex, string operations, parsing)
- Size checks (length, count, capacity)

```yaml
CONSTRAINTS:
  - "price: must be non-negative number"
  - "percentage: integer between 0 and 100 inclusive"
```

### Step 5: Identify EDGE_CASES

Look for:
- Boundary values handled in conditions (`>=`, `<`, `==`)
- Special cases (empty input, null/nil/None/undefined, zero, max value)
- Comments mentioning edge cases
- Guard clauses at the top of the function

```yaml
EDGE_CASES:
  - "empty string: returns error"
  - "percentage = 0: returns original price"
  - "percentage = 100: returns 0.0"
```

### Step 6: Generate TESTS

Create test cases that cover:
1. **Happy path** — normal inputs that succeed (2-3 tests)
2. **Boundary** — values at the edges of conditions (2-3 tests)
3. **Error cases** — inputs that trigger each error branch (1 per branch)

```yaml
TESTS:
  # Happy path
  - "calculate_discount(100.0, 20) == 80.0"
  - "calculate_discount(50.0, 10) == 45.0"

  # Boundary
  - "calculate_discount(100.0, 0) == 100.0"
  - "calculate_discount(100.0, 100) == 0.0"

  # Error cases
  - "calculate_discount(-10.0, 20) raises error"
  - "calculate_discount(100.0, -5) raises error"
```

### Step 7: Add Metadata

```yaml
DEPENDENCIES:
  - "library_name"  # only external imports/packages used by the function

COMPLEXITY:
  time: O(n)  # analyze loops and recursion
  space: O(1) # analyze allocations
```

### Step 8: Assemble and Validate

Combine all sections into a complete spec. Then self-validate:
- Does every BEHAVIOR rule have at least one test?
- Does every EDGE_CASE have a test?
- Do CONSTRAINTS map to BEHAVIOR rules?
- Is INTENT free of implementation details?

---

## Output Format

Ask the user which format they prefer. Default to the format used elsewhere in their project.

Set `meta.language` to the language detected from the source code.

**YAML format:**
```yaml
---
meta:
  name: function_name
  language: <detected from source>
  version: 1.0
  tags: [inferred, tags]
---

RUNE: function_name

SIGNATURE: |
  ...
INTENT: |
  ...
BEHAVIOR:
  - ...
TESTS:
  - ...
# ... remaining fields
```

**Markdown format:**
```markdown
### function_name

**SIGNATURE:** `...`

**INTENT:** ...

**BEHAVIOR:**
- WHEN ... THEN ...

**TESTS:**
- `...`
```

---

## Rules

- Extract behavior from the code AS-IS — do not improve or fix the function
- If the code has bugs, note them but spec the current behavior
- Preserve exact error messages from the source code
- If types are not annotated, infer and mark with a comment
- Always generate at least 3 tests per function
- Use the source language's syntax for SIGNATURE, not pseudocode
- Works with any programming language — adapt extraction to the language's idioms
- Ask the user to verify the spec matches their intent — code might not reflect original requirements
