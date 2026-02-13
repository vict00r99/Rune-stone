# Full Project Example: Online Bookstore Orders

This example demonstrates the complete RUNE pipeline from business requirements to tested code.

## The Pipeline

```
REQUIREMENTS.md  ──▶  specs/*.rune  ──▶  src/*.py  ──▶  tests/*.py
   (Analyst)        (Analyst + AI)   (Developer + AI) (Developer + AI)
```

### Step 1: Analyst writes requirements

The analyst produces [REQUIREMENTS.md](REQUIREMENTS.md) — a plain-language document describing what the system should do. No code, no technical spec. Just business rules and examples.

### Step 2: Analyst + AI generates RUNE specs

The analyst feeds the requirements to an AI assistant (Claude, GPT, Cursor) with the RUNE skill loaded. The AI translates each requirement into a formal `.rune` specification:

- [specs/calculate_order_total.rune](specs/calculate_order_total.rune) — from requirement "Calculate Order Total"
- [specs/validate_coupon.rune](specs/validate_coupon.rune) — from requirement "Validate Coupon"
- [specs/check_free_shipping.rune](specs/check_free_shipping.rune) — from requirement "Check Free Shipping"

Each spec contains the exact signature, behavior rules, constraints, edge cases, and test cases — all derived from the business rules.

### Step 3: Developer + AI generates implementation

The developer gives the `.rune` specs to their AI coding tool. The AI generates implementations that follow the spec exactly:

- [src/order_total.py](src/order_total.py) — implements calculate_order_total.rune
- [src/coupon.py](src/coupon.py) — implements validate_coupon.rune
- [src/shipping.py](src/shipping.py) — implements check_free_shipping.rune

### Step 4: Developer + AI generates tests

From the same specs, the AI generates a complete test suite:

- [tests/test_order_total.py](tests/test_order_total.py) — 10 tests from spec
- [tests/test_coupon.py](tests/test_coupon.py) — 9 tests from spec
- [tests/test_shipping.py](tests/test_shipping.py) — 9 tests from spec

## Directory Structure

```
full-project/
├── README.md                           # This file
├── REQUIREMENTS.md                     # Step 1: Business requirements
├── specs/
│   ├── calculate_order_total.rune      # Step 2: Formal specs
│   ├── validate_coupon.rune
│   └── check_free_shipping.rune
├── src/
│   ├── order_total.py                  # Step 3: Implementations
│   ├── coupon.py
│   └── shipping.py
└── tests/
    ├── test_order_total.py             # Step 4: Test suites
    ├── test_coupon.py
    └── test_shipping.py
```

## Running the Tests

```bash
cd examples/full-project
pip install pytest
pytest tests/ -v
```

## Why This Works

The `.rune` spec acts as a **contract** between analyst and developer:

- **Analyst** defines *what* the code should do (behavior, constraints, edge cases)
- **Developer** defines *how* the code does it (implementation, architecture, patterns)
- **AI** translates in both directions — requirements to spec, spec to code
- **Tests** are generated automatically from the spec, not invented after the fact

The spec is the single source of truth. If requirements change, update the spec, regenerate the code.

## Try It Yourself

1. Read [REQUIREMENTS.md](REQUIREMENTS.md)
2. Give it to your AI assistant with: *"Generate RUNE specs from these requirements"*
3. Compare what you get with the specs in `specs/`
4. Then ask: *"Generate Python code from calculate_order_total.rune"*
5. Compare with `src/order_total.py`

For the complete setup guide (what to upload, what prompts to use, how to iterate), see the [Workflow Guide](../../docs/workflow.md).
