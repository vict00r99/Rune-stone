# Project Instructions for Claude

## Development Standards

All functions in this project must be specified using the RUNE pattern before implementation. RUNE is a specification pattern that provides a structured contract between human intent and AI implementation. Specs can be written as `.rune` YAML files or as Markdown sections.

## RUNE Specification Format

When I provide a `.rune` file or ask you to create one, follow this structure:

```yaml
---
meta:
  name: function_name
  language: python
  version: 1.0
  tags: [relevant, tags]
---

RUNE: function_name

SIGNATURE: |
  def function_name(param: type) -> return_type

INTENT: |
  Clear 1-3 sentence description of what the function does.

BEHAVIOR:
  - WHEN condition THEN action
  - WHEN another_condition THEN another_action
  - OTHERWISE default_action

CONSTRAINTS:
  - "param: specific constraint"

EDGE_CASES:
  - "case: expected behavior"

TESTS:
  - "test assertion or description"
  - "another test case"
  - "error case test"

DEPENDENCIES: []

EXAMPLES:
  - |
    # Usage example with expected output

COMPLEXITY:
  time: O(?)
  space: O(?)
```

## Implementation Rules

When implementing from a RUNE spec:

1. **Read the entire spec carefully** before writing any code
2. **Follow SIGNATURE exactly** -- use the exact function name, parameter names, types, and return type
3. **Implement all BEHAVIOR rules** -- translate each WHEN/THEN rule into code logic
4. **Handle all EDGE_CASES** -- every listed edge case must be handled explicitly
5. **Validate CONSTRAINTS** -- add input validation for every constraint listed
6. **Include all TESTS** -- generate a test function for every item in the TESTS section
7. **Add docstring from INTENT** -- use the INTENT text as the function's docstring
8. **Match COMPLEXITY** -- if complexity is specified, ensure your implementation meets it

## When Creating RUNE Specs

If I ask you to create a new RUNE spec:

1. Ask clarifying questions about edge cases and constraints if anything is ambiguous
2. Generate a complete spec with **all** required fields (meta, RUNE, SIGNATURE, INTENT, BEHAVIOR, TESTS)
3. Include at least 3 test cases covering: happy path, boundary conditions, and error cases
4. Be explicit about edge cases -- list every boundary condition
5. Use actual Python syntax in SIGNATURE (not pseudocode)
6. Keep INTENT concise (1-3 sentences) and put detailed logic in BEHAVIOR

## Workflow

### Implementing an existing spec

```
User: "Implement api_client.rune"

Steps:
1. Read the spec from project knowledge
2. Generate the function matching SIGNATURE exactly
3. Add docstring from INTENT
4. Implement all BEHAVIOR rules as code logic
5. Add input validation from CONSTRAINTS
6. Handle every EDGE_CASE
7. Generate pytest test functions from TESTS
8. Verify implementation matches COMPLEXITY requirements
```

### Creating a new spec then implementing

```
User: "I need a function to parse CSV files with header detection"

Steps:
1. Ask clarifying questions if needed
2. Generate complete RUNE spec
3. Present spec for review
4. After approval, generate implementation + tests
```

### Updating an existing spec

```
User: "Add retry logic to api_client.rune"

Steps:
1. Read the current spec
2. Update SIGNATURE if parameters change
3. Add new BEHAVIOR rules
4. Add new EDGE_CASES
5. Add new TESTS
6. Present updated spec
7. Regenerate implementation from updated spec
```

## Project Specs

This project includes the following RUNE specifications in the `specs/` directory:

- **api_client.rune** -- HTTP client for making API requests with error handling
- **data_validator.rune** -- Schema-based data validation with constraint checking

Upload these as project knowledge files so they are available in every conversation.

## Code Style

- Python 3.11+ with type hints on all functions
- Use `async`/`await` for I/O-bound operations
- pytest for all test files
- Google-style docstrings derived from INTENT field
