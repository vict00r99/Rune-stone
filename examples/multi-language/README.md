# Multi-Language Example: One Spec, Two Languages

This example demonstrates RUNE's language-agnostic nature. A single `.rune` spec produces consistent implementations in different languages.

## The Spec

[`slugify.rune`](slugify.rune) defines a function that converts text into URL-friendly slugs. The spec uses `language: any` and a language-neutral signature:

```
function slugify(text: string, separator: string = "-") -> string
```

The behavior, constraints, edge cases, and tests are the same regardless of target language.

## The Implementations

### Python

```python
# python/slugify.py
def slugify(text: str, separator: str = "-") -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9\s-]", "", ascii_text.lower())
    ...
```

Uses `unicodedata.normalize()` from the standard library for accent removal.

### TypeScript

```typescript
// typescript/slugify.ts
export function slugify(text: string, separator: string = "-"): string {
    let slug = text.split("").map(c => ACCENT_MAP[c] ?? c).join("");
    slug = slug.toLowerCase().replace(/[^a-z0-9\s-]/g, "");
    ...
```

Uses a character map for accent replacement (no native NFKD in browser JS).

## Same Tests, Same Results

Both implementations pass the exact same test cases from the spec:

| Test | Python | TypeScript |
|------|--------|------------|
| `slugify("Hello World")` | `"hello-world"` | `"hello-world"` |
| `slugify("Café Résumé")` | `"cafe-resume"` | `"cafe-resume"` |
| `slugify("  too   many   spaces  ")` | `"too-many-spaces"` | `"too-many-spaces"` |
| `slugify("Hello World", "_")` | `"hello_world"` | `"hello_world"` |

Different languages, different idioms, same behavior. That's the point.

## Running the Tests

**Python:**
```bash
cd examples/multi-language/python
pip install pytest
pytest test_slugify.py -v
```

**TypeScript:**
```bash
cd examples/multi-language/typescript
npm install --save-dev typescript jest ts-jest @types/jest
npx jest slugify.test.ts
```

## Directory Structure

```
multi-language/
├── README.md               # This file
├── slugify.rune            # Language-agnostic spec
├── python/
│   ├── slugify.py          # Python implementation
│   └── test_slugify.py     # Python tests (pytest)
└── typescript/
    ├── slugify.ts          # TypeScript implementation
    └── slugify.test.ts     # TypeScript tests (Jest)
```

## Key Takeaway

The `.rune` spec defines **what** the function does. Each language decides **how**:

- Python uses `unicodedata` for Unicode normalization
- TypeScript uses a character map for accent replacement
- Both produce identical output for identical input

The spec is the contract. The implementation is the language's job.
