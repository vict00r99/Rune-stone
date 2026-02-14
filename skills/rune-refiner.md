# RUNE Refiner Skill

Analyzes existing RUNE specifications and suggests concrete improvements. Unlike the validator (which checks rules), the refiner identifies weaknesses and proposes specific content to strengthen the spec.

---

## How to Use

When given a RUNE spec that is structurally valid but may be incomplete or weak, analyze it and suggest improvements with ready-to-use content.

Input: a `.rune` YAML file or Markdown spec section.
Output: a list of actionable suggestions with proposed content.

---

## Analysis Areas

### 1. Test Coverage Gaps

Check if the TESTS section adequately covers the BEHAVIOR rules.

**Look for:**
- BEHAVIOR rules with only 1 test (should have 2+)
- Missing boundary tests for numeric ranges
- Missing empty/null input tests
- Missing tests for the OTHERWISE clause
- Happy path tests that only cover one scenario

**Example suggestion:**
```markdown
**Gap:** BEHAVIOR rule "WHEN percentage > 100 THEN raise error" has only 1 test with value 101.
**Suggestion:** Add a test with a more extreme value:
  - `"calculate_discount(100.0, 150) raises ValueError"`
```

### 2. Edge Case Discovery

Identify edge cases the spec author may have missed.

**Common edge cases by input type** (adapt null/empty representations to the target language):

| Type | Edge cases to check |
|------|-------------------|
| string | empty `""`, whitespace-only, very long (>1000 chars), unicode, null/nil/None |
| integer | 0, negative, max value for the language, null/nil/None |
| decimal/float | 0.0, negative, very small (0.001), very large, NaN, Infinity, null/nil/None |
| list/array | empty, single item, duplicate items, null/nil/None |
| map/object | empty, missing keys, extra keys, null/nil/None |
| boolean | both true and false |
| date/time | today, past, far future, midnight, timezone boundaries |

**Example suggestion:**
```markdown
**Gap:** No edge case for whitespace-only input.
**Suggestion:** Add to EDGE_CASES:
  - `"whitespace-only email ('   '): returns (False, 'Email cannot be empty')"`
And add to TESTS:
  - `"validate_email('   ')[0] == False"`
```

### 3. BEHAVIOR Ambiguity

Identify behavior rules that are vague or open to multiple interpretations.

**Red flags:**
- Rules without specific error messages: `THEN raise error`
- Rules with vague conditions: `WHEN input is invalid`
- Rules that use "etc." or "and so on"
- Missing OTHERWISE clause
- Conditions that could overlap (multiple rules match the same input)

**Example suggestion:**
```markdown
**Ambiguity:** "WHEN input is invalid THEN raise error" — what makes input invalid? What error?
**Suggestion:** Replace with specific rules:
  - `WHEN input is empty THEN raise error "Input cannot be empty"`
  - `WHEN input contains non-ASCII characters THEN raise error "Input must be ASCII"`
```

### 4. CONSTRAINTS Completeness

Check if CONSTRAINTS fully describe the valid input space.

**Look for:**
- Parameters without any constraint
- Constraints that are vague ("must be valid")
- Missing range information for numeric parameters
- Missing format information for string parameters
- Missing size limits for collections

**Example suggestion:**
```markdown
**Gap:** Parameter `timeout` has no constraint.
**Suggestion:** Add to CONSTRAINTS:
  - `"timeout: integer between 1 and 300 (seconds)"`
```

### 5. INTENT Clarity

Check if INTENT clearly communicates purpose.

**Issues to flag:**
- Implementation details (mentioning regex, algorithms, libraries)
- Too vague ("processes data")
- Missing return value description
- More than 3 sentences

### 6. Spec Consistency

Check internal consistency across sections.

**Look for:**
- EDGE_CASES that aren't reflected in BEHAVIOR
- CONSTRAINTS that imply behavior not in BEHAVIOR
- EXAMPLES that show behavior not in BEHAVIOR
- COMPLEXITY that doesn't match the apparent algorithm

---

## Output Format

```markdown
## RUNE Refinement Report: `<function_name>`

### Test Coverage
1. **[ADD TEST]** BEHAVIOR rule "WHEN percentage > 100..." has 1 test. Add:
   - `"calculate_discount(100.0, 200) raises ValueError"`

2. **[ADD TEST]** OTHERWISE clause has no dedicated test. Add:
   - `"calculate_discount(100.0, 20) == 80.0"` (if not already present)

### Edge Cases
3. **[ADD EDGE_CASE]** No test for zero price:
   - Edge case: `"price = 0.0: returns 0.0 regardless of percentage"`
   - Test: `"calculate_discount(0.0, 50) == 0.0"`

4. **[ADD EDGE_CASE]** No test for float precision:
   - Edge case: `"rounding: 10.0 * 33% = 6.70, not 6.7"`
   - Test: `"calculate_discount(10.0, 33) == 6.70"`

### Ambiguity
5. **[CLARIFY]** BEHAVIOR rule "WHEN coupon has expired" — expired means `expires_at < current_date` or `expires_at <= current_date`? Add to EDGE_CASES:
   - `"expires today: still valid (expires_at == current_date)"`

### Constraints
6. **[ADD CONSTRAINT]** Parameter `date` has no format constraint. Add:
   - `"date: ISO 8601 string (YYYY-MM-DD)"`

### Summary
- **Suggestions:** 6 total (2 tests, 2 edge cases, 1 clarification, 1 constraint)
- **Estimated strength improvement:** The spec goes from covering ~70% of realistic inputs to ~95%
```

---

## Rules

- Only suggest improvements, never modify the spec directly
- Every suggestion must include ready-to-paste content (YAML or Markdown)
- Prioritize suggestions that prevent real bugs over stylistic improvements
- Do not suggest changes that contradict existing BEHAVIOR rules
- If the spec is already strong, say so — don't invent unnecessary suggestions
- Focus on gaps that would cause different AI tools to generate different behavior
