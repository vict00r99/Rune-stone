# Before & After: AI Code Generation with RUNE

A side-by-side comparison of real AI coding workflows — without specs vs with RUNE.

---

## Scenario: "Build a coupon validation function"

### WITHOUT RUNE

You tell the AI:

> "Write a function to validate coupon codes"

**Developer A gets:**

```python
def check_coupon(coupon_code, coupons):
    for c in coupons:
        if c["code"] == coupon_code:
            return c
    return None
```

No input validation. No expiration check. Returns `None` on failure (not descriptive). Case-sensitive comparison.

**Developer B gets:**

```python
def validate_coupon(code: str, coupon_list: list) -> dict:
    """Validates a coupon code."""
    if not code:
        raise ValueError("Code required")
    for coupon in coupon_list:
        if coupon["code"].lower() == code.lower():
            if coupon["active"]:
                return {"valid": True, "coupon": coupon}
    return {"valid": False, "reason": "Not found"}
```

Different function name. Different return type. Checks `active` flag instead of expiration date. No discount value validation.

**Developer C gets:**

```python
class CouponValidator:
    def __init__(self, coupons):
        self.coupons = {c["code"]: c for c in coupons}

    def validate(self, code):
        coupon = self.coupons.get(code.upper())
        if not coupon:
            return False, "Invalid coupon"
        if coupon["expired"]:
            return False, "Expired"
        return True, coupon
```

Now it's a class. Different field names (`expired` vs `expires_at`). Pre-indexes coupons in a dict. Completely different interface.

**Three developers, three AI tools, three different functions. None of them match. None have tests.**

---

### WITH RUNE

The analyst writes the requirement. The AI generates a spec:

```yaml
RUNE: validate_coupon

SIGNATURE: |
  def validate_coupon(code: str, active_coupons: list[dict], current_date: str) -> tuple[bool, dict | str]

BEHAVIOR:
  - WHEN code is empty THEN return (False, "Coupon code cannot be empty")
  - WHEN code not found (case-insensitive) THEN return (False, "Coupon code not found")
  - WHEN coupon has expired THEN return (False, "Coupon has expired")
  - WHEN discount value is invalid THEN return (False, "Invalid discount value")
  - OTHERWISE return (True, matching_coupon)

TESTS:
  - "validate_coupon('SAVE10', [...], '2025-01-15')[0] == True"
  - "validate_coupon('save10', [...], '2025-01-15')[0] == True"   # case-insensitive
  - "validate_coupon('OLD', [...], '2025-01-15')[0] == False"     # expired
  - "validate_coupon('', [], '2025-01-15')[0] == False"           # empty code
```

**Developer A, B, and C all get:**

```python
def validate_coupon(code, active_coupons, current_date):
    if not code:
        return (False, "Coupon code cannot be empty")

    code_upper = code.upper()
    match = None
    for coupon in active_coupons:
        if coupon["code"].upper() == code_upper:
            match = coupon
            break

    if match is None:
        return (False, "Coupon code not found")

    if match["expires_at"] < current_date:
        return (False, "Coupon has expired")

    # ... validation continues per spec

    return (True, match)
```

Same function name. Same signature. Same return type. Same behavior. Same edge cases handled. Tests included.

---

## Scenario: "Calculate order totals"

### WITHOUT RUNE

> "Write a function to calculate order totals with tax"

**Result 1:** Takes a flat list of prices, hardcodes 8% tax.
**Result 2:** Takes item objects with quantities, tax as parameter, but no input validation.
**Result 3:** Returns a dict with subtotal/tax/total breakdown, rounds differently.

No two implementations agree on the interface, let alone the behavior.

### WITH RUNE

The spec defines:

```yaml
SIGNATURE: |
  def calculate_order_total(items: list[dict], tax_rate: float) -> float

CONSTRAINTS:
  - "items: each with 'price' (float > 0) and 'quantity' (int > 0)"
  - "tax_rate: float between 0 and 25"
```

Every AI tool, every developer, every time: same inputs, same outputs, same validation, same rounding.

---

## Scenario: "Add this to multiple languages"

### WITHOUT RUNE

You ask for Python, then TypeScript, then Go. Each time you re-explain the requirements. Each time the AI interprets them slightly differently. The Python version validates inputs, the TypeScript version doesn't. The Go version handles an edge case the others miss.

### WITH RUNE

One `slugify.rune` spec with `language: any`. Feed it to the AI with "implement in Python" or "implement in TypeScript". Both implementations handle the same edge cases, pass the same tests, produce the same output for the same input. ([See the example](../examples/multi-language/))

---

## The Difference, Summarized

|  | Without RUNE | With RUNE |
|--|-------------|-----------|
| **Interface** | Every AI invents its own | Defined once in the spec |
| **Edge cases** | Whatever the AI remembers | Enumerated in EDGE_CASES |
| **Error messages** | Generic or missing | Specified in BEHAVIOR |
| **Tests** | Written after (maybe) | Generated from TESTS section |
| **Cross-team consistency** | None | Everyone uses the same contract |
| **Cross-language consistency** | Re-explain each time | Same spec, any language |
| **Requirement traceability** | Lost in chat history | REQUIREMENTS.md → .rune → code |
| **What changes when requirements change?** | Start over | Update the spec, regenerate |

---

## Try It

1. Open your AI tool and ask: *"Write a function to validate email addresses"*
2. Do it 3 times. Compare the results.
3. Now give it [`validate_email.rune`](../examples/basic/validate_email.rune) and ask: *"Implement this spec"*
4. Do it 3 times. Compare the results.

The difference is the spec.
