# Integrating RUNE with agents.md

This guide shows how to use RUNE specifications with agents.md architecture for building multi-agent systems.

## Overview

**agents.md** defines the architecture of your agent system (who does what), while **RUNE** defines the contracts for each agent's tools (how they work).

Together, they provide:
- ✅ Clear separation between architecture and implementation
- ✅ Reviewable specifications before coding
- ✅ Consistent tool interfaces
- ✅ Comprehensive testing built-in

## Quick Example

### agents.md (High-level architecture)

```markdown
## Code Reviewer Agent

**Role:** Reviews Python code for quality issues

**Capabilities:**
- Check code style compliance
- Validate test coverage
- Detect code smells

**Tools:**
- validate_test_coverage → [spec](tools/test_validator.rune)
- generate_docstring → [spec](tools/doc_generator.rune)

**Workflow:**
```
User submits code
  ↓
Validate test coverage
  ↓
Generate documentation
  ↓
Return comprehensive report
```
```

### RUNE spec (Tool contract)

```yaml
# tools/test_validator.rune
---
meta:
  name: validate_test_coverage
  language: python
  agent: test_validator_agent
---

RUNE: validate_test_coverage

SIGNATURE: |
  def validate_test_coverage(source_code: str, test_code: str) -> dict[str, Any]

INTENT: |
  Tool for Code Reviewer Agent.
  Checks Python code against PEP 8 style guidelines.

BEHAVIOR:
  - WHEN code is empty THEN return {valid: True, violations: []}
  - PARSE code with flake8
  - COLLECT all style violations
  - RETURN structured report

TESTS:
  - "check_style_compliance('x = 1')['valid'] == True"
  - "check_style_compliance('x=1')['valid'] == False"
# ... rest of spec
```

## Step-by-Step Integration

### Step 1: Define Your Agent Architecture

Create `agents.md` with your agent definitions:

```markdown
# Multi-Agent System

## Agents

### Agent 1: Code Generator
**Capabilities:** Generate functions from specifications
**Tools:** generate_implementation, generate_tests

### Agent 2: Code Reviewer
**Capabilities:** Review and improve code quality
**Tools:** validate_rune_spec, run_spec_tests, check_implementation_compliance

### Agent 3: Documentation Generator
**Capabilities:** Generate and update documentation
**Tools:** generate_integration_guide, update_readme

## Workflow

User request → Code Generator → generates code →
Code Reviewer → validates → Documentation Generator → complete
```

### Step 2: Create RUNE Specs for Each Tool

For each tool in each agent, create a RUNE spec:

```
project/
├── agents.md
└── tools/
    ├── generate_implementation.rune
    ├── generate_tests.rune
    ├── validate_rune_spec.rune
    ├── run_spec_tests.rune
    ├── check_implementation_compliance.rune
    ├── enhance_rune_spec.rune
    └── update_readme.rune
```

### Step 3: Link Specs in agents.md

Reference the RUNE specs in your agent definitions:

```markdown
## Code Generator Agent

**Tools:**
- generate_implementation → [spec](tools/generate_implementation.rune) - Generate function from spec
- generate_tests → [spec](tools/generate_tests.rune) - Generate test suite
```

### Step 4: Review Specs Before Implementation

Team reviews RUNE specs:
- Are inputs/outputs clear?
- Are edge cases covered?
- Are tests comprehensive?
- Is behavior well-defined?

This catches issues **before** any code is written.

### Step 5: Generate Implementations

Use AI to generate implementations from RUNE specs:

```bash
# With Claude
for spec in tools/*.rune; do
    claude "Generate Python implementation from $spec"
done

# With Cursor
# Open each .rune file and use Cmd+K: "Generate implementation"
```

### Step 6: Implement Agent Logic

Agents import and use the generated tools:

```python
# agents/code_reviewer.py
from tools.implementations import check_style_compliance, validate_tests

class CodeReviewerAgent:
    def review_code(self, code: str) -> dict:
        # Use tools generated from RUNE specs
        style_report = check_style_compliance(code)
        test_report = validate_tests(code)
        
        return {
            "style": style_report,
            "tests": test_report,
            "overall": self._generate_summary(style_report, test_report)
        }
```

## Complete Example

See [`examples/integrations/agents-md-example/`](../examples/integrations/agents-md-example/) for a full working example.

### Directory Structure

```
agents-md-example/
├── agents.md                    # Agent definitions
├── README.md                    # Setup instructions
├── tools/                       # RUNE specifications
│   ├── test_validator.rune
│   └── doc_generator.rune
└── implementations/             # Generated code
    ├── test_validator.py
    └── doc_generator.py
```

## Best Practices

### 1. Use meta.agent field

Link RUNE specs to their agent:

```yaml
---
meta:
  name: tool_name
  language: python
  agent: code_reviewer_agent  # ← Links to agent
---
```

### 2. Tool naming convention

Use verb_noun format:
- ✅ `check_style_compliance`
- ✅ `validate_test_coverage`
- ✅ `generate_docstring`
- ❌ `style` (too vague)
- ❌ `validator` (not a verb)

### 3. Reference specs in agents.md

Always link to the RUNE spec:

```markdown
**Tools:**
- tool_name → [spec](path/to/tool.rune) - Brief description
```

This makes it easy to find the contract for each tool.

### 4. One tool = One RUNE spec

Don't combine multiple tools in one spec. Keep them focused:

❌ Bad:
```yaml
RUNE: code_quality_checker
# Does style, tests, AND documentation
```

✅ Good:
```yaml
# test_validator.rune
RUNE: validate_test_coverage

# doc_generator.rune
RUNE: generate_docstring
```

### 5. Version your specs

When tools change, update the spec first:

```yaml
---
meta:
  version: 2.0  # ← Increment when behavior changes
---
```

## Workflows

### Workflow 1: New Agent Tool

```
1. Define capability in agents.md
2. Create RUNE spec for tool
3. Review spec with team
4. Generate implementation with AI
5. Test implementation
6. Agent uses tool
```

### Workflow 2: Modify Existing Tool

```
1. Update RUNE spec (increment version)
2. Review changes
3. Regenerate implementation
4. Run tests (from spec)
5. Deploy updated tool
```

### Workflow 3: Multi-Agent Collaboration

```yaml
# Agent A's tool output becomes Agent B's tool input

# tools/analyze_code.rune (Agent A)
SIGNATURE: def analyze_code(code: str) -> CodeAnalysis

# tools/fix_issues.rune (Agent B)
SIGNATURE: def fix_issues(analysis: CodeAnalysis) -> str
```

Specs ensure compatible interfaces between agents.

## Common Patterns

### Pattern 1: Tool with Options

```yaml
SIGNATURE: |
  def tool_name(
      input: str,
      options: dict[str, Any] | None = None
  ) -> Result
```

Allows agents to customize tool behavior.

### Pattern 2: Tool with Callbacks

```yaml
SIGNATURE: |
  def tool_name(
      input: str,
      on_progress: Callable[[str], None] | None = None
  ) -> Result
```

Agents can monitor long-running tools.

### Pattern 3: Tool Chaining

```yaml
# First tool
SIGNATURE: def extract_data(source: str) -> RawData

# Second tool  
SIGNATURE: def transform_data(raw: RawData) -> CleanData

# Third tool
SIGNATURE: def load_data(clean: CleanData) -> bool
```

Agent orchestrates the pipeline.

## Benefits Summary

| Aspect | Without RUNE | With RUNE |
|--------|-------------|-----------|
| Tool contracts | Implicit, in code | Explicit, reviewable |
| Consistency | Each tool different | Standard structure |
| Testing | Often missing | Built into spec |
| Documentation | Separate docs | Self-documenting |
| Review process | Review code | Review specs first |
| Modifications | Change code directly | Update spec, regenerate |

## Troubleshooting

### Issue: Generated code doesn't match spec

**Solution:** Regenerate with more explicit prompt:
```
"Generate implementation from this RUNE spec. Follow the BEHAVIOR section exactly."
```

### Issue: Agent tools have incompatible interfaces

**Solution:** Define shared types in RUNE specs:
```yaml
# In both specs
CONSTRAINTS:
  - "Returns CodeAnalysis type with fields: issues, metrics, suggestions"
```

### Issue: Too many small tools

**Solution:** Group related functionality:
```yaml
RUNE: code_quality_checker
# Has methods: check_style(), check_tests(), check_docs()
```

## Resources

- [agents.md specification](https://github.com/e2b-dev/agent-protocol)
- [Example multi-agent system](../examples/integrations/agents-md-example/)
- [RUNE templates](../templates/)

## Next Steps

1. Review the [complete example](../examples/integrations/agents-md-example/)
2. Try creating a simple 2-agent system
3. Define agent tools as RUNE specs
4. Generate and test implementations

---

**Questions?** Open an issue or start a discussion on GitHub!