# Tools

## Validator

[`validate.py`](validate.py) — CLI tool for validating `.rune` files against the RUNE spec standard.

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

### CI/CD integration

Add to your pipeline to reject PRs with invalid specs:

```yaml
# GitHub Actions example
- name: Validate RUNE specs
  run: python tools/validate.py --strict specs/
```

## Parser

[`parser.py`](parser.py) — Python library for parsing `.rune` files into structured objects.

```python
from parser import parse_rune_file, parse_rune_string, RUNEParser

# Parse from file
spec = parse_rune_file("specs/calculate_discount.rune")
print(spec.name)        # "calculate_discount"
print(spec.language)    # "python"
print(spec.signature)   # "def calculate_discount(price: float, percentage: int) -> float"
print(spec.test_count)  # 15
print(spec.is_async)    # False

# Parse from string
spec = parse_rune_string(yaml_content)

# Validate
parser = RUNEParser()
spec = parser.parse_file("my_spec.rune")
errors = parser.validate(spec)
if errors:
    for err in errors:
        print(f"  {err}")
```

### Dependencies

Both tools require `pyyaml`:

```bash
pip install pyyaml
```
