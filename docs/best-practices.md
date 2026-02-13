# RUNE Best Practices

This guide contains best practices, patterns, and recommendations for writing effective RUNE specifications.

## Table of Contents

- [General Principles](#general-principles)
- [Writing Good Signatures](#writing-good-signatures)
- [Defining Clear Behavior](#defining-clear-behavior)
- [Comprehensive Testing](#comprehensive-testing)
- [Edge Cases and Constraints](#edge-cases-and-constraints)
- [Documentation](#documentation)
- [Common Patterns](#common-patterns)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Language-Specific Guidelines](#language-specific-guidelines)

---

## General Principles

### 1. Specification First, Implementation Second

Always write the RUNE spec before implementing:

✅ **Good workflow:**
```
1. Write RUNE spec
2. Review with team
3. Generate implementation
4. Run tests from spec
```

❌ **Bad workflow:**
```
1. Write code
2. Try to document after
3. Create spec retroactively
```

### 2. Be Explicit, Not Implicit

Don't leave behavior open to interpretation:

❌ **Bad (implicit):**
```yaml
BEHAVIOR:
  - Process the input
  - Return the result
```

✅ **Good (explicit):**
```yaml
BEHAVIOR:
  - WHEN input is empty THEN raise ValueError("Input cannot be empty")
  - PARSE input using JSON decoder
  - VALIDATE parsed data against schema
  - TRANSFORM data to output format
  - RETURN transformed data with metadata
```

### 3. Think in Tests

Write your TESTS section first, then define BEHAVIOR to make them pass:

```yaml
# Start with tests
TESTS:
  - "validate_email('user@example.com') == (True, '')"
  - "validate_email('invalid') == (False, 'Missing @ symbol')"
  - "validate_email('') == (False, 'Email cannot be empty')"

# Then define behavior to satisfy tests
BEHAVIOR:
  - WHEN email is empty THEN return (False, "Email cannot be empty")
  - WHEN email does not contain @ THEN return (False, "Missing @ symbol")
  - WHEN email matches RFC 5322 THEN return (True, "")
```

### 4. One Function, One Responsibility

Keep specs focused on a single, clear purpose:

❌ **Bad (too many responsibilities):**
```yaml
RUNE: process_user_data
# Validates, transforms, saves to DB, sends email, logs...
```

✅ **Good (single responsibility):**
```yaml
RUNE: validate_user_data
# Only validates

RUNE: transform_user_data
# Only transforms

RUNE: save_user_data
# Only saves
```

---

## Writing Good Signatures

### Use Actual Language Syntax

Always write SIGNATURE in the target language's actual syntax:

#### Python
```yaml
✅ Good:
SIGNATURE: |
  def calculate_total(
      items: list[dict[str, Any]],
      tax_rate: float = 0.0,
      discount: float | None = None
  ) -> dict[str, float]

❌ Bad:
SIGNATURE: function calculate_total(items, tax_rate, discount) -> result
```

#### TypeScript
```yaml
✅ Good:
SIGNATURE: |
  function calculateTotal(
    items: Array<Record<string, any>>,
    taxRate: number = 0.0,
    discount?: number
  ): Record<string, number>

❌ Bad:
SIGNATURE: calculateTotal(items, taxRate, discount)
```

#### Go
```yaml
✅ Good:
SIGNATURE: |
  func CalculateTotal(
    items []map[string]interface{},
    taxRate float64,
    discount *float64
  ) (map[string]float64, error)

❌ Bad:
SIGNATURE: CalculateTotal(items, taxRate, discount) result
```

### Include Type Information

Always specify types, even in dynamically-typed languages:

```yaml
# Python - use type hints
SIGNATURE: def process(data: dict[str, Any]) -> ProcessResult

# JavaScript/TypeScript - use JSDoc or TS types
SIGNATURE: |
  /**
   * @param {Object} data
   * @returns {ProcessResult}
   */
  function process(data)
```

### Use Default Values Appropriately

```yaml
✅ Good (sensible defaults):
SIGNATURE: |
  def fetch_data(
      url: str,
      timeout: int = 30,
      retries: int = 3
  ) -> Response

❌ Bad (everything required):
SIGNATURE: |
  def fetch_data(
      url: str,
      timeout: int,
      retries: int,
      headers: dict,
      verify_ssl: bool
  ) -> Response
```

---

## Defining Clear Behavior

### Use WHEN/THEN/OTHERWISE Format

This makes logic flow explicit:

```yaml
BEHAVIOR:
  - WHEN condition_1 THEN action_1
  - WHEN condition_2 THEN action_2
  - WHEN condition_3 THEN action_3
  - OTHERWISE default_action
```

### Example: Input Validation

```yaml
✅ Good:
BEHAVIOR:
  - WHEN age < 0 THEN raise ValueError("Age cannot be negative")
  - WHEN age > 150 THEN raise ValueError("Age must be realistic")
  - WHEN 0 <= age < 18 THEN return "minor"
  - WHEN 18 <= age < 65 THEN return "adult"
  - OTHERWISE return "senior"

❌ Bad:
BEHAVIOR:
  - Validate age
  - Return appropriate category
```

### Break Down Complex Logic

For complex functions, use numbered steps:

```yaml
BEHAVIOR:
  - STEP 1: Validate inputs
    - WHEN input_a is None THEN raise ValueError
    - WHEN input_b < 0 THEN raise ValueError
  
  - STEP 2: Process data
    - PARSE input_a as JSON
    - TRANSFORM parsed data
    - FILTER results by criteria
  
  - STEP 3: Format output
    - CONVERT to target format
    - ADD metadata
    - RETURN formatted result
```

### Specify Error Conditions

Always specify what errors should be raised:

```yaml
BEHAVIOR:
  - WHEN file_path does not exist THEN raise FileNotFoundError
  - WHEN file is not readable THEN raise PermissionError
  - WHEN file is empty THEN raise ValueError("File is empty")
  - WHEN file format is invalid THEN raise ValueError("Invalid format")
  - OTHERWISE read and process file
```

---

## Comprehensive Testing

### Minimum Test Coverage

Every RUNE spec should have **at least 3 test categories:**

```yaml
TESTS:
  # 1. Happy path - normal usage
  - "function(valid_input) == expected_output"
  
  # 2. Boundary conditions
  - "function(min_value) == expected"
  - "function(max_value) == expected"
  
  # 3. Error cases
  - "function(invalid_input) raises ExpectedException"
```

### Test Organization

Group tests by category for clarity:

```yaml
TESTS:
  # Happy path
  - "calculate_discount(100, 10) == 90.0"
  - "calculate_discount(50, 20) == 40.0"
  
  # Boundary conditions
  - "calculate_discount(100, 0) == 100.0"
  - "calculate_discount(100, 100) == 0.0"
  - "calculate_discount(0.01, 10) == 0.009"
  
  # Error cases
  - "calculate_discount(-10, 10) raises ValueError"
  - "calculate_discount(100, -5) raises ValueError"
  - "calculate_discount(100, 150) raises ValueError"
  
  # Edge cases
  - "calculate_discount(0, 50) == 0.0"
  - "calculate_discount(float('inf'), 10) raises ValueError"
```

### Use Descriptive Test Names

```yaml
✅ Good (descriptive):
TESTS:
  - "parses valid ISO 8601 date string correctly"
  - "raises ValueError when date format is invalid"
  - "handles timezone information properly"

❌ Bad (vague):
TESTS:
  - "test1 passes"
  - "works correctly"
  - "handles errors"
```

### Test All Branches

Ensure every branch in BEHAVIOR has a test:

```yaml
BEHAVIOR:
  - WHEN status == "active" THEN return True     # ← needs test
  - WHEN status == "pending" THEN return False   # ← needs test
  - OTHERWISE raise ValueError                    # ← needs test

TESTS:
  - "check_status('active') == True"      # ✓
  - "check_status('pending') == False"    # ✓
  - "check_status('invalid') raises ValueError"  # ✓
```

---

## Edge Cases and Constraints

### Document All Edge Cases

Think about boundary conditions:

```yaml
EDGE_CASES:
  # Empty inputs
  - "empty string: raises ValueError"
  - "empty list: returns empty result"
  - "empty dict: uses default values"
  
  # Null/None
  - "None input: raises ValueError"
  - "None in list: filters out"
  
  # Boundaries
  - "minimum value: inclusive"
  - "maximum value: exclusive"
  - "zero: special handling"
  
  # Type issues
  - "wrong type: raises TypeError"
  - "mixed types in list: converts or raises"
  
  # Size limits
  - "very large input (>1GB): raises ValueError"
  - "very long string (>10000 chars): truncates"
```

### Explicit Constraints

Be specific about input constraints:

```yaml
✅ Good (specific):
CONSTRAINTS:
  - "email: must match RFC 5322 format, max 254 chars"
  - "age: integer between 0 and 150 inclusive"
  - "password: min 8 chars, must contain uppercase, lowercase, digit, special char"
  - "filename: no path separators, max 255 chars, valid UTF-8"

❌ Bad (vague):
CONSTRAINTS:
  - "email: must be valid"
  - "age: must be reasonable"
  - "password: must be strong"
  - "filename: must be valid"
```

---

## Documentation

### Write Intent for Humans

INTENT should be clear to non-developers:

```yaml
✅ Good (clear):
INTENT: |
  Sends a welcome email to newly registered users.
  Email includes account activation link and getting started guide.
  Returns True if email sent successfully, False otherwise.

❌ Bad (technical):
INTENT: |
  Calls SMTP server with templated HTML body containing JWT token
  and markdown-rendered guide, returns boolean.
```

### Include Usage Examples

Provide realistic examples:

```yaml
EXAMPLES:
  - |
    # Basic usage
    result = send_welcome_email(
        email="user@example.com",
        username="Alice"
    )
    if result:
        print("Welcome email sent!")
  
  - |
    # With custom template
    result = send_welcome_email(
        email="user@example.com",
        username="Bob",
        template="premium_welcome"
    )
  
  - |
    # Error handling
    try:
        send_welcome_email(email="invalid-email")
    except ValueError as e:
        print(f"Failed to send: {e}")
```

### Document Complexity

Help users understand performance:

```yaml
COMPLEXITY:
  time: O(n log n)  # where n is number of items to sort
  space: O(n)       # creates copy of input array
```

---

## Common Patterns

### Pattern 1: Validation Function

```yaml
RUNE: validate_input

SIGNATURE: |
  def validate_input(data: dict) -> tuple[bool, str]

BEHAVIOR:
  - VALIDATE each field in data
  - COLLECT all validation errors
  - WHEN no errors THEN return (True, "")
  - OTHERWISE return (False, error_message)

TESTS:
  - "validate_input(valid_data) == (True, '')"
  - "validate_input(invalid_data)[0] == False"
```

### Pattern 2: Data Transformation

```yaml
RUNE: transform_data

SIGNATURE: |
  def transform_data(input: RawData) -> CleanData

BEHAVIOR:
  - PARSE input data
  - CLEAN and normalize values
  - TRANSFORM to target schema
  - VALIDATE output
  - RETURN transformed data

TESTS:
  - "output has correct schema"
  - "handles missing fields"
  - "preserves important data"
```

### Pattern 3: Async Operation

```yaml
RUNE: fetch_data

SIGNATURE: |
  async def fetch_data(url: str, timeout: int = 30) -> Response

BEHAVIOR:
  - VALIDATE url format
  - CREATE async HTTP request
  - WHEN timeout exceeded THEN raise TimeoutError
  - WHEN request fails THEN raise RequestError
  - PARSE response
  - RETURN parsed data

TESTS:
  - "await fetch_data(valid_url) returns data"
  - "await fetch_data(invalid_url) raises ValueError"
  - "await fetch_data(url, timeout=1) raises TimeoutError"
```

### Pattern 4: Builder/Factory

```yaml
RUNE: create_config

SIGNATURE: |
  def create_config(
      env: str,
      overrides: dict | None = None
  ) -> Config

BEHAVIOR:
  - LOAD default config for environment
  - WHEN overrides provided THEN merge with defaults
  - VALIDATE final config
  - RETURN Config object

TESTS:
  - "create_config('dev') has dev defaults"
  - "create_config('prod', overrides) merges correctly"
```

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Vague Behavior

```yaml
❌ Bad:
BEHAVIOR:
  - Process the data
  - Handle errors
  - Return result

✅ Good:
BEHAVIOR:
  - PARSE data as JSON
  - WHEN parsing fails THEN raise ValueError with details
  - VALIDATE parsed structure
  - WHEN validation fails THEN raise ValidationError
  - TRANSFORM to output format
  - RETURN transformed data
```

### ❌ Anti-Pattern 2: Missing Error Cases

```yaml
❌ Bad:
TESTS:
  - "function(valid_input) works"

✅ Good:
TESTS:
  - "function(valid_input) == expected"
  - "function(None) raises ValueError"
  - "function('') raises ValueError"
  - "function(invalid_type) raises TypeError"
```

### ❌ Anti-Pattern 3: Implementation Details in Intent

```yaml
❌ Bad:
INTENT: |
  Uses regex pattern ^[\w\.-]+@[\w\.-]+\.\w+$ to validate email,
  compiled with re.IGNORECASE flag, matching against RFC 5322.

✅ Good:
INTENT: |
  Validates email addresses according to RFC 5322 standards.
  Returns True if valid, False otherwise.
```

### ❌ Anti-Pattern 4: Too Many Responsibilities

```yaml
❌ Bad:
RUNE: process_user_request
# Validates, authenticates, processes, logs, sends email, updates DB...

✅ Good:
# Split into focused functions
RUNE: validate_user_request
RUNE: authenticate_user
RUNE: process_request
RUNE: log_request
RUNE: send_notification
RUNE: update_database
```

### ❌ Anti-Pattern 5: Insufficient Test Coverage

```yaml
❌ Bad (only 1 test):
TESTS:
  - "function works"

✅ Good (comprehensive):
TESTS:
  # Happy path (2-3 tests)
  - "function(valid_input1) == expected1"
  - "function(valid_input2) == expected2"
  
  # Boundaries (2-3 tests)
  - "function(min_value) == expected"
  - "function(max_value) == expected"
  
  # Errors (2-3 tests)
  - "function(invalid_input) raises Exception"
  - "function(None) raises ValueError"
```

---

## Language-Specific Guidelines

### Python

```yaml
# Use type hints
SIGNATURE: def func(x: int) -> str

# Follow PEP 8 naming
RUNE: calculate_total  # not calculateTotal

# Document exceptions
BEHAVIOR:
  - WHEN x < 0 THEN raise ValueError

# Use standard library types
dict[str, Any]  # not Dict (deprecated)
list[int]       # not List
```

### TypeScript

```yaml
# Use TypeScript types
SIGNATURE: function func(x: number): Promise<string>

# Use camelCase
RUNE: calculateTotal  # not calculate_total

# Async functions
SIGNATURE: async function fetchData(url: string): Promise<Data>

# Union types
param: string | null
```

### Go

```yaml
# Return errors explicitly
SIGNATURE: func ProcessData(data []byte) (Result, error)

# Use exported names
RUNE: ProcessData  # not processData

# Pointer receivers
SIGNATURE: func (c *Config) Validate() error
```

---

## Checklist for Review

Before finalizing a RUNE spec, check:

- [ ] All required fields present (SIGNATURE, INTENT, BEHAVIOR, TESTS — plus meta and RUNE header for YAML format)
- [ ] SIGNATURE uses correct language syntax
- [ ] BEHAVIOR uses WHEN/THEN format
- [ ] At least 3 test cases (happy path, boundary, error)
- [ ] All EDGE_CASES documented
- [ ] CONSTRAINTS are specific
- [ ] INTENT is clear and concise
- [ ] EXAMPLES show realistic usage
- [ ] No implementation details in INTENT
- [ ] Single, focused responsibility

---

## Resources

- [RUNE Specification](../SPEC.md)
- [Getting Started Guide](getting-started.md)
- [Example Library](examples.md)
- [Templates](../templates/)

**Questions?** Open an issue or discussion on GitHub!