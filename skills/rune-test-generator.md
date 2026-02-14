# RUNE Test Generator Skill

Generates complete, runnable test files from RUNE specifications. Converts pseudo-assertions from the TESTS section into real test code with concrete fixtures, proper assertions, and framework-specific structure. Works with any language and testing framework.

---

## How to Use

When given a RUNE spec (`.rune` file or Markdown section), generate a complete test file for the target language's testing framework.

Input: a RUNE spec + target language/framework (or auto-detect from project).
Output: a complete, runnable test file.

---

## Framework Detection

Auto-detect the testing framework from project files when possible. Common examples:

| Signal | Framework |
|--------|-----------|
| `pytest.ini`, `pyproject.toml` with `[tool.pytest]` | pytest (Python) |
| `jest.config.*` | Jest (JS/TS) |
| `vitest.config.*` | Vitest (JS/TS) |
| `go.mod` | Go testing |
| `Cargo.toml` | Rust #[test] |
| `pom.xml`, `build.gradle` | JUnit (Java/Kotlin) |
| `Package.swift` | XCTest (Swift) |
| `mix.exs` | ExUnit (Elixir) |
| `*.cabal`, `stack.yaml` | Hspec/HUnit (Haskell) |
| `composer.json` | PHPUnit (PHP) |
| `Gemfile` | RSpec/Minitest (Ruby) |
| `.csproj` | xUnit/NUnit (C#) |

This list is not exhaustive. Any language with a testing framework is supported — adapt the output to the framework's conventions. If unclear, ask the user.

---

## Process

### Step 1: Parse the Spec

Extract from the RUNE spec:
- **Function name** from SIGNATURE
- **Parameters and types** from SIGNATURE
- **Test cases** from TESTS section
- **Edge cases** from EDGE_CASES section
- **Constraints** from CONSTRAINTS section (for fixture data)
- **Error types** from BEHAVIOR (for exception/error assertions)

### Step 2: Expand `[...]` into Fixtures

The `[...]` notation in RUNE tests is shorthand for "representative data matching CONSTRAINTS." Expand it into concrete test fixtures using the target language's idioms.

**From spec:**
```yaml
CONSTRAINTS:
  - "coupons: list of dicts with keys code, discount_type, discount_value, expires_at"

TESTS:
  - "validate_coupon('SAVE10', [...], '2025-01-15')[0] == True"
```

**Python (pytest):**
```python
@pytest.fixture
def sample_coupons():
    return [
        {"code": "SAVE10", "discount_value": 10, "expires_at": "2025-12-31"},
        {"code": "OLD", "discount_value": 5, "expires_at": "2024-01-01"},  # expired
    ]
```

**Go:**
```go
func sampleCoupons() []Coupon {
    return []Coupon{
        {Code: "SAVE10", DiscountValue: 10, ExpiresAt: "2025-12-31"},
        {Code: "OLD", DiscountValue: 5, ExpiresAt: "2024-01-01"}, // expired
    }
}
```

**TypeScript (Jest):**
```typescript
const sampleCoupons = [
  { code: "SAVE10", discountValue: 10, expiresAt: "2025-12-31" },
  { code: "OLD", discountValue: 5, expiresAt: "2024-01-01" }, // expired
];
```

Rules for expanding `[...]`:
- Read CONSTRAINTS to understand the data structure
- Read EDGE_CASES to include boundary data
- Create minimal fixtures — only the data needed for the tests
- Name fixtures descriptively
- Include comments explaining why each item exists

### Step 3: Generate Test Functions

Convert each pseudo-assertion into a test function using the target framework.

**From spec:**
```yaml
TESTS:
  - "calculate_discount(100.0, 20) == 80.0"
  - "calculate_discount(-10.0, 20) raises error"
```

**Python (pytest):**
```python
def test_discount_normal():
    assert calculate_discount(100.0, 20) == 80.0

def test_discount_negative_price_raises():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_discount(-10.0, 20)
```

**TypeScript (Jest):**
```typescript
test("calculates discount for normal values", () => {
  expect(calculateDiscount(100.0, 20)).toBe(80.0);
});

test("throws on negative price", () => {
  expect(() => calculateDiscount(-10.0, 20)).toThrow("Price cannot be negative");
});
```

**Go:**
```go
func TestDiscountNormal(t *testing.T) {
    result, err := CalculateDiscount(100.0, 20)
    if err != nil { t.Fatal(err) }
    if result != 80.0 { t.Errorf("expected 80.0, got %f", result) }
}

func TestDiscountNegativePriceErrors(t *testing.T) {
    _, err := CalculateDiscount(-10.0, 20)
    if err == nil { t.Fatal("expected error for negative price") }
}
```

**Rust:**
```rust
#[test]
fn test_discount_normal() {
    assert_eq!(calculate_discount(100.0, 20).unwrap(), 80.0);
}

#[test]
fn test_discount_negative_price_errors() {
    assert!(calculate_discount(-10.0, 20).is_err());
}
```

### Step 4: Organize Test Structure

Group tests by category using the target framework's grouping mechanism:

- **pytest**: comments or classes
- **Jest/Vitest**: `describe()` blocks
- **Go**: subtests with `t.Run()`
- **Rust**: `mod tests` with named functions
- **JUnit**: `@Nested` classes
- **RSpec**: `context` blocks
- **ExUnit**: `describe` blocks

### Step 5: Add EDGE_CASE Tests

If the spec has EDGE_CASES, generate additional tests for each. Skip edge case tests that duplicate existing tests from the TESTS section.

---

## Output Format

Generate a complete file with:

1. **Imports** — framework imports + function import
2. **Fixtures** — expanded `[...]` data
3. **Test functions** — grouped by category
4. **File header** — comment referencing the source spec

Follow the target language's naming convention for test files and functions.

---

## Rules

- Generate ONLY test code, not the implementation
- Every test must be independently runnable
- Use the exact error messages from BEHAVIOR for exception/error matching
- Import path should match the project's module structure — ask the user if unclear
- Do not skip any test from the TESTS section
- Do not invent tests beyond what the spec defines (unless EDGE_CASES suggest them)
- Floating point comparisons: use the framework's approximate comparison (pytest.approx, closeTo, delta, etc.)
- Adapt error assertion style to the language: exceptions (Python/Java/TS), error returns (Go), Result type (Rust), pattern match (Elixir/Haskell)
- Any language with a testing framework is supported — follow its conventions
