# agents.md Integration Example

A complete example showing how to use RUNE specifications with agents.md architecture for a multi-agent code quality system.

## What This Demonstrates

- Defining agent roles and workflows in `agents.md`
- Specifying each agent's tools as RUNE specs
- Linking RUNE specs from agent definitions
- Multi-agent coordination for code review

## Files

| File | Description |
|------|-------------|
| `agents.md` | Agent system architecture with 2 agents |
| `tools/doc_generator.rune` | RUNE spec for docstring generation tool |
| `tools/test_validator.rune` | RUNE spec for test coverage validation tool |

## Agents

### Documentation Agent

Generates Python docstrings in Google, NumPy, or Sphinx styles. Analyzes function signatures, parameters, and body logic to produce accurate documentation.

**Tool:** `generate_docstring` ([spec](tools/doc_generator.rune))

### Test Validator Agent

Validates test coverage by comparing source code against test files. Reports coverage percentage, identifies missing tests, and provides actionable recommendations.

**Tool:** `validate_test_coverage` ([spec](tools/test_validator.rune))

## How It Works

1. `agents.md` defines the agent architecture -- who does what
2. Each tool references a `.rune` file that defines the contract -- how it works
3. RUNE specs are reviewed before any code is written
4. Implementations are generated from the approved specs
5. Agents use the generated tool implementations in their workflows

## Usage

### With Claude Code

```bash
# Generate a docstring
claude "Read tools/doc_generator.rune and generate a Google-style docstring for this function: def add(a: int, b: int) -> int: return a + b"

# Validate test coverage
claude "Read tools/test_validator.rune and validate the test coverage of my_module.py"
```

### With Claude Projects

1. Upload `agents.md` and both `.rune` files to project knowledge
2. Ask Claude to perform code reviews using the agent pipeline

### Generating Implementations

```bash
# Generate the doc_generator tool implementation
claude "Generate a Python implementation from tools/doc_generator.rune"

# Generate the test_validator tool implementation
claude "Generate a Python implementation from tools/test_validator.rune"
```

## Extending This Example

To add a new agent or tool:

1. Define the agent in `agents.md` with its role, capabilities, and tools
2. Create a `.rune` file for each tool in `tools/`
3. Link the spec from the agent definition: `tool_name --> [spec](tools/tool.rune)`
4. Review the spec, then generate the implementation

## Related

- [RUNE + agents.md Guide](../../../docs/integration-agents-md.md)
- [Agent Tool Template](../../../templates/agent-tool.rune)
- [RUNE Specification](../../../SPEC.md)
