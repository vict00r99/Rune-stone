# RUNE Diff Skill

Compares a RUNE specification against its implementation to detect drift. Use this skill to verify that code still matches its spec after modifications, or to audit existing implementations.

---

## How to Use

When given a RUNE spec and its corresponding implementation file, compare them and report every discrepancy.

Input: a RUNE spec (`.rune` or Markdown) + an implementation file (`.py`, `.ts`, `.go`, etc.).
Output: a diff report listing all mismatches.

---

## Comparison Areas

### 1. SIGNATURE Match

Compare the spec's SIGNATURE against the actual function declaration.

**Check:**
- Function name matches exactly
- Parameter names match
- Parameter types match
- Parameter order matches
- Return type matches
- Default values match

**Example mismatch:**
```markdown
**SIGNATURE MISMATCH**
- Spec:  `def validate_coupon(code: str, coupons: list[dict], date: str) -> tuple[bool, str]`
- Code:  `def validate_coupon(coupon_code: str, coupon_list: list, current_date: str) -> dict`
- Issues:
  - Parameter renamed: `code` → `coupon_code`
  - Parameter renamed: `coupons` → `coupon_list`
  - Parameter renamed: `date` → `current_date`
  - Type changed: `coupons` lost `[dict]` annotation
  - Return type changed: `tuple[bool, str]` → `dict`
```

### 2. BEHAVIOR Coverage

For each WHEN/THEN rule in the spec, verify the implementation handles it.

**Process:**
1. List every BEHAVIOR rule from the spec
2. Find the corresponding code branch (if/elif/else, match/case, guard clause)
3. Verify the action matches (return value, exception type, error message)

**Check:**
- Every BEHAVIOR rule has a corresponding code branch
- The condition logic matches the spec
- The action (return/raise) matches the spec
- Error messages are character-for-character identical
- The ORDER of checks matches the spec (top to bottom)

**Example mismatch:**
```markdown
**BEHAVIOR DRIFT**
- Rule: `WHEN code is empty THEN return (False, "Coupon code cannot be empty")`
- Code: `if not code: raise ValueError("Code required")`
- Issues:
  - Action changed: spec says `return (False, ...)` but code `raises ValueError`
  - Message changed: `"Coupon code cannot be empty"` → `"Code required"`
```

### 3. Error Message Accuracy

Extract all error messages from the implementation and compare against BEHAVIOR.

**Check:**
- Every error message in the code appears in the spec
- Every error message in the spec appears in the code
- Messages match exactly (no typos, no rephrasing)

### 4. CONSTRAINTS Enforcement

For each CONSTRAINT in the spec, check if the implementation validates it.

**Check:**
- Each constraint has a validation check in the code
- The validation rejects the right inputs
- Constraints not in BEHAVIOR (preconditions) are documented but not necessarily enforced

**Example mismatch:**
```markdown
**MISSING CONSTRAINT CHECK**
- Spec CONSTRAINT: `"email: maximum 254 characters (RFC 5321)"`
- Code: No length check found
- Impact: Emails longer than 254 chars will be accepted
```

### 5. EDGE_CASES Handling

For each EDGE_CASE in the spec, verify the implementation handles it correctly.

**Check:**
- The implementation produces the expected result for each edge case
- No edge cases are silently ignored

### 6. Extra Behavior (not in spec)

Identify behavior in the code that is NOT described in the spec.

**Look for:**
- Extra validation checks not in CONSTRAINTS or BEHAVIOR
- Additional error conditions
- Default values or fallback behavior not in the spec
- Logging, caching, or side effects not mentioned

**Example:**
```markdown
**UNDOCUMENTED BEHAVIOR**
- Code has: `if len(email) > 254: return (False, "Email too long")`
- Spec: No BEHAVIOR rule or CONSTRAINT mentions max length
- Action: Add to spec or remove from code
```

---

## Output Format

```markdown
## RUNE Diff Report: `<function_name>`

**Spec:** `validate_coupon.rune`
**Code:** `src/coupon.py`

### SIGNATURE
- [MATCH] Function name: `validate_coupon`
- [MATCH] Parameters: `code`, `coupons`, `date`
- [DRIFT] Return type: spec says `tuple[bool, str]`, code returns `tuple[bool, dict | str]`

### BEHAVIOR
| Rule | Status | Detail |
|------|--------|--------|
| WHEN code is empty... | MATCH | Line 12 |
| WHEN code not found... | MATCH | Line 18 |
| WHEN coupon expired... | DRIFT | Message differs: "Coupon has expired" vs "Expired coupon" |
| OTHERWISE... | MATCH | Line 28 |

### ERROR MESSAGES
- [DRIFT] Line 22: `"Expired coupon"` should be `"Coupon has expired"`

### CONSTRAINTS
- [MATCH] code: non-empty string
- [MISSING] code: case-insensitive — code uses exact match instead

### EDGE_CASES
- [MATCH] empty code: handled
- [DRIFT] expires today: spec says "still valid" but code treats it as expired

### UNDOCUMENTED
- Line 8: `if not isinstance(code, str): raise TypeError` — not in spec

### Summary
- **Status:** DRIFT DETECTED
- **Matches:** 7
- **Drifts:** 3 (return type, error message, expiration logic)
- **Missing:** 1 (case-insensitive matching)
- **Undocumented:** 1 (type check)
- **Recommendation:** Update spec to match code, OR fix code to match spec (see details above)
```

---

## Severity Levels

- **MATCH** — Spec and code agree.
- **DRIFT** — Spec and code disagree. Must be resolved (update one or the other).
- **MISSING** — Spec describes behavior the code doesn't implement.
- **UNDOCUMENTED** — Code has behavior the spec doesn't describe.

---

## Rules

- Report findings, do not modify either the spec or the code
- Be precise: include line numbers from the implementation
- For each DRIFT, state clearly what the spec says vs what the code does
- Do not assume which side is "correct" — the user decides whether to update the spec or the code
- If the code has multiple implementations of the same spec (e.g., Python + TypeScript), compare each separately
