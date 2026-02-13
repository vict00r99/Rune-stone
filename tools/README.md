# Tools

## Validation Script

[`validate.py`](validate.py) is a standalone CLI tool for validating `.rune` files:

```bash
# Validate a single spec
python tools/validate.py examples/basic/calculate_discount.rune

# Validate all specs in a directory
python tools/validate.py examples/

# Strict mode (checks optional fields too)
python tools/validate.py --strict examples/basic/validate_email.rune

# JSON output for CI/CD
python tools/validate.py --json examples/ > validation-report.json
```

## Agent Tool Specs

Example RUNE specifications for AI agent tools have been moved to [`examples/tool-specs/`](../examples/tool-specs/). These demonstrate how to specify tool contracts for multi-agent systems.
