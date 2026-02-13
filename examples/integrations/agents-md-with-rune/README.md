# AGENTS.md + RUNE Integration Example

This example shows how to embed RUNE specs directly inside an AGENTS.md file.

## The Idea

Instead of maintaining separate `.rune` files, you can add a `## Function Specifications` section to your AGENTS.md. Each function spec uses the same RUNE pattern (SIGNATURE, BEHAVIOR, TESTS, EDGE_CASES) but in Markdown format.

## How It Works

The [AGENTS.md](AGENTS.md) in this directory defines:
- **Project context** — language, framework, conventions
- **3 function specs** — calculate_order_total, validate_coupon, check_free_shipping

Any AI agent that reads the AGENTS.md gets both the project context AND the function contracts.

## Usage

```
"Implement the calculate_order_total spec from AGENTS.md"
```

The AI reads the AGENTS.md, finds the spec, and generates an implementation that follows the BEHAVIOR rules and passes the TESTS.

## When to Use This Format

- You already use AGENTS.md for project context
- You have a handful of key functions to specify
- You want zero extra files or tooling
- Your team uses different AI tools and you want one source of truth

For larger projects with many specs, consider using standalone `.rune` files alongside your AGENTS.md. See [examples/full-project/](../../full-project/) for that approach.
