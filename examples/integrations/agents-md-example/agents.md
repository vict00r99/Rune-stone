# Code Quality Agent System

Multi-agent system for automated code review, documentation, and test validation.

---

## System Overview

This system uses two specialized agents to review and improve Python code quality. Each agent has RUNE-specified tools that define clear contracts for their capabilities.

### Agents

1. **Documentation Agent** -- Generates and validates code documentation
2. **Test Validator Agent** -- Validates test coverage and completeness

---

## Agent Definitions

### 1. Documentation Agent

**Role:** Generates comprehensive documentation for Python code

**Capabilities:**
- Generate docstrings in multiple styles (Google, NumPy, Sphinx)
- Analyze function signatures and behavior
- Include usage examples in generated docs

**Tools:**
- `generate_docstring` --> [spec](tools/doc_generator.rune) -- Generate docstrings from function code

**Workflow:**
```
Receive function code
  |
  v
Parse function signature and body
  |
  v
Generate docstring in requested style:
  - Google style (default)
  - NumPy style
  - Sphinx style
  |
  v
Optionally include usage examples
  |
  v
Return formatted docstring
```

**Guidelines:**
- Always analyze the full function body, not just the signature
- Generate examples that demonstrate actual function behavior
- Handle async functions, generators, and class methods
- Default to Google style if not specified

---

### 2. Test Validator Agent

**Role:** Validates test coverage and identifies gaps

**Capabilities:**
- Analyze source code to identify testable functions and branches
- Compare against existing test code
- Calculate coverage metrics
- Recommend specific missing test cases

**Tools:**
- `validate_test_coverage` --> [spec](tools/test_validator.rune) -- Validate test completeness

**Workflow:**
```
Receive source code + test code
  |
  v
Parse source to extract functions, branches, edge cases
  |
  v
Parse tests to identify covered scenarios
  |
  v
Calculate coverage percentage
  |
  v
Identify missing tests:
  - Untested functions
  - Untested branches
  - Missing edge cases
  - Missing error cases
  |
  v
Generate recommendations
  |
  v
Return structured report
```

**Guidelines:**
- Minimum recommended coverage: 80%
- Always check for happy path, boundary, and error test cases
- Flag test functions without assertions as incomplete
- Provide actionable recommendations, not vague suggestions

---

## Multi-Agent Workflow

### Code Review Pipeline

```
Developer submits code for review
  |
  v
Test Validator Agent:
  - Analyzes source code structure
  - Compares against test suite
  - Reports coverage gaps
  |
  v
Documentation Agent:
  - Checks for missing docstrings
  - Generates documentation for undocumented functions
  |
  v
Combined report:
  - Test coverage: X%
  - Missing tests: [list]
  - Missing docs: [list]
  - Recommendations: [list]
```

---

## Agent Coordination Rules

1. **Test Validator runs first** -- coverage data informs documentation priorities
2. **Documentation Agent second** -- generates docs for validated code
3. **Reports are merged** -- single unified quality report returned to developer
4. **Iterative** -- developer fixes issues, agents re-validate until passing

---

## Quality Standards

### Test Coverage
- Minimum 80% coverage for all modules
- Every public function must have at least one test
- Error paths must be tested

### Documentation
- Every public function must have a docstring
- Docstrings must include parameter documentation
- Complex functions must include usage examples

---

## Usage with Claude Code

```bash
# Generate docstring for a function
claude "Use doc_generator.rune to document this function: [paste code]"

# Validate test coverage
claude "Use test_validator.rune to check coverage of module.py against test_module.py"

# Full code review
claude "Run the code quality pipeline on src/ and tests/"
```

---

## Project Structure

```
agents-md-example/
├── agents.md                    # This file
├── README.md                    # Setup instructions
└── tools/
    ├── doc_generator.rune       # Documentation generation tool spec
    └── test_validator.rune      # Test validation tool spec
```
