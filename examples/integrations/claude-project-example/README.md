# Claude Projects Integration Example

A complete example showing how to use RUNE specifications with Claude Projects for consistent code generation.

## What This Demonstrates

- Setting up a Claude Project with RUNE-aware custom instructions
- Uploading RUNE specs as project knowledge files
- Workflow for implementing code from specs
- Workflow for creating new specs and iterating

## Files

| File | Description |
|------|-------------|
| `project_instructions.md` | Custom instructions to paste into your Claude Project |
| `specs/api_client.rune` | RUNE spec for an async HTTP JSON client |
| `specs/data_validator.rune` | RUNE spec for schema-based data validation |

## Setup

### 1. Create a Claude Project

Go to [claude.ai](https://claude.ai) and create a new Project.

### 2. Add Custom Instructions

Copy the contents of `project_instructions.md` into your project's **Custom Instructions** field.

### 3. Upload Knowledge Files

Upload the following files to **Project Knowledge**:

- `specs/api_client.rune`
- `specs/data_validator.rune`

### 4. Start a Conversation

Try these prompts:

```
"Implement api_client.rune"
```

```
"Implement data_validator.rune with full pytest test suite"
```

```
"Create a RUNE spec for a function that parses ISO 8601 date strings"
```

```
"Does this implementation match data_validator.rune?" [paste code]
```

## Example Conversations

### Implementing from a spec

> **You:** Implement api_client.rune
>
> **Claude:** Reads the spec, generates a complete `fetch_json()` implementation with httpx, input validation for all constraints, error handling for HTTP status codes, and a full pytest test suite covering all 12 test cases from the spec.

### Creating a new spec

> **You:** I need a RUNE spec for a function that hashes passwords using bcrypt
>
> **Claude:** Asks about salt rounds preference, generates a complete RUNE spec with SIGNATURE, BEHAVIOR rules for input validation, TESTS for happy path / empty input / Unicode, and EDGE_CASES for very long passwords.

### Comparing spec to implementation

> **You:** Does this code match api_client.rune? [pastes code]
>
> **Claude:** Compares the code against the spec, identifies that the timeout validation is missing and two edge cases are unhandled, suggests specific fixes.

## Directory Structure

```
claude-project-example/
├── README.md                  # This file
├── project_instructions.md    # Claude Project custom instructions
└── specs/
    ├── api_client.rune        # HTTP client specification
    └── data_validator.rune    # Data validation specification
```

## Tips

- **Start with specs**: Always write a RUNE spec before asking Claude to implement
- **Upload new specs**: When Claude generates a spec you approve, download and upload it to project knowledge
- **Reference by name**: Say "Implement api_client.rune" rather than "implement the API client"
- **Iterate on specs**: Ask Claude to update specs when requirements change, then regenerate the implementation

## Related

- [Using RUNE with AI Tools](../../../docs/using-skills-with-other-tools.md#claude-projects)
- [RUNE Specification](../../../SPEC.md)
- [Basic Function Template](../../../templates/basic-function.rune)
