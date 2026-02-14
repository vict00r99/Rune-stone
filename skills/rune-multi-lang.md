# RUNE Multi-Language Skill

Generates implementations and tests from a single RUNE spec in multiple programming languages simultaneously. Use this skill when a spec has `language: any` or when the user needs the same function in several languages.

---

## How to Use

When given a RUNE spec and a list of target languages, generate an implementation + test file for each language, ensuring all implementations produce identical behavior.

Input: a RUNE spec + list of target languages.
Output: one implementation file + one test file per language.

---

## Language Adaptation

Any programming language is supported. When generating for a target language, adapt:

- **Naming convention** — follow the language's standard (snake_case, camelCase, PascalCase, etc.)
- **Error handling** — use the language's idiomatic mechanism (exceptions, error returns, Result types, pattern matching)
- **Testing framework** — use the language's standard or most common framework
- **Type system** — map types to native equivalents

---

## Process

### Step 1: Analyze the Spec

Read the RUNE spec and extract:
- Function purpose (from INTENT)
- Input/output contract (from SIGNATURE, even if language-specific)
- All behavior rules (from BEHAVIOR)
- All test cases (from TESTS)
- Constraints and edge cases

### Step 2: Adapt Signature Per Language

Convert the SIGNATURE to each target language's syntax and conventions.

**From a spec with:**
```yaml
SIGNATURE: |
  def calculate_discount(price: float, percentage: int) -> float
```

**Generate:**

| Language | Adapted Signature |
|----------|------------------|
| Python | `def calculate_discount(price: float, percentage: int) -> float` |
| TypeScript | `function calculateDiscount(price: number, percentage: number): number` |
| Go | `func CalculateDiscount(price float64, percentage int) (float64, error)` |
| Rust | `fn calculate_discount(price: f64, percentage: i32) -> Result<f64, String>` |
| Java | `public static double calculateDiscount(double price, int percentage)` |

**Adaptation rules:**
- Follow each language's naming convention (snake_case, camelCase, PascalCase)
- Map types to native equivalents (`float` → `f64`, `number`, `double`)
- Add error return channels where idiomatic (Go returns `error`, Rust returns `Result`)
- Use the language's exception/error mechanism for BEHAVIOR error rules

### Step 3: Adapt Error Handling

Each language handles errors differently. Adapt the BEHAVIOR error rules:

| Spec says | Python | TypeScript | Go | Rust |
|-----------|--------|------------|-----|------|
| `raise ValueError("msg")` | `raise ValueError("msg")` | `throw new Error("msg")` | `return 0, fmt.Errorf("msg")` | `return Err("msg".to_string())` |

Preserve the exact error messages across all languages.

### Step 4: Generate Implementations

For each language, generate the implementation following these rules:
- Implement ALL BEHAVIOR rules in order
- Use idiomatic patterns for the target language
- Preserve the logic flow from the spec
- Match error messages exactly
- Handle all EDGE_CASES
- Add a docstring/comment from INTENT

### Step 5: Generate Tests

For each language, generate a complete test file:
- Convert every TESTS entry to the language's test framework
- Expand `[...]` into concrete fixtures per language
- Use language-idiomatic assertion style
- Group tests by category (happy path, boundary, error)

### Step 6: Cross-Language Verification Table

After generating all implementations, produce a verification table:

```markdown
## Cross-Language Verification

| Test Case | Python | TypeScript | Go | Rust |
|-----------|--------|------------|-----|------|
| `(100.0, 20) → 80.0` | `calculate_discount(100.0, 20)` | `calculateDiscount(100.0, 20)` | `CalculateDiscount(100.0, 20)` | `calculate_discount(100.0, 20)` |
| `(-10.0, 20) → error` | `raises ValueError` | `throws Error` | `returns error` | `returns Err` |
| ... | ... | ... | ... | ... |

All implementations must produce **identical outputs** for identical inputs.
Error messages must be **character-for-character identical** across languages.
```

---

## Output Structure

Generate files organized by language:

```
<function_name>/
├── python/
│   ├── <function_name>.py
│   └── test_<function_name>.py
├── typescript/
│   ├── <function_name>.ts
│   └── <function_name>.test.ts
├── go/
│   ├── <function_name>.go
│   └── <function_name>_test.go
└── VERIFICATION.md          # cross-language verification table
```

Or if adding to an existing project, follow the project's directory structure.

---

## Type Mapping Reference

| RUNE / Python | TypeScript | Go | Rust | Java |
|--------------|------------|-----|------|------|
| `str` | `string` | `string` | `String` / `&str` | `String` |
| `int` | `number` | `int` / `int64` | `i32` / `i64` | `int` / `long` |
| `float` | `number` | `float64` | `f64` | `double` |
| `bool` | `boolean` | `bool` | `bool` | `boolean` |
| `list[T]` | `Array<T>` / `T[]` | `[]T` | `Vec<T>` | `List<T>` |
| `dict[K, V]` | `Record<K, V>` | `map[K]V` | `HashMap<K, V>` | `Map<K, V>` |
| `tuple[A, B]` | `[A, B]` | `(A, B)` via struct/returns | `(A, B)` | custom class |
| `None` / `null` | `null` / `undefined` | `nil` | `None` (Option) | `null` |
| `Optional[T]` | `T \| null` | `*T` | `Option<T>` | `Optional<T>` |

---

## Rules

- All implementations must pass the same logical tests
- Error messages must be identical across languages (same string)
- Use idiomatic patterns per language — do not write "Python in Go"
- If a RUNE feature cannot be directly expressed in a language (e.g., tuples in Java), use the closest idiomatic equivalent and document the adaptation
- Always generate the cross-language verification table
- If the spec has `language: <specific>`, ask the user which additional languages they want
- If the spec has `language: any`, ask the user which languages to target (or default to Python + TypeScript)
