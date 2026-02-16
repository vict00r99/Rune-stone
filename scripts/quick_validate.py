#!/usr/bin/env python3
"""
Quick validation script for RUNE skills in Anthropic SKILL.md format.

Based on the Anthropic skills spec:
https://github.com/anthropics/skills/tree/main/skills/skill-creator

Usage:
    python scripts/quick_validate.py [skills_directory]
    python scripts/quick_validate.py              # defaults to skills/
"""

import sys
import os
import re
from pathlib import Path


ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def parse_frontmatter(content):
    """Parse YAML frontmatter without PyYAML dependency."""
    if not content.startswith("---"):
        return None, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format (missing closing ---)"

    frontmatter = {}
    current_key = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key_match = re.match(r"^(\S[\w-]*)\s*:\s*(.*)", line)
        if key_match:
            current_key = key_match.group(1)
            value = key_match.group(2).strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            frontmatter[current_key] = value
        elif current_key and line.startswith("  "):
            frontmatter[current_key] += " " + line.strip()

    return frontmatter, None


def validate_skill(skill_path):
    """Validate a single skill directory. Returns (passed, errors, warnings)."""
    skill_path = Path(skill_path)
    errors = []
    warnings = []

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md not found"], []

    content = skill_md.read_text(encoding="utf-8")

    # Parse frontmatter
    frontmatter, err = parse_frontmatter(content)
    if err:
        return False, [err], []

    # Check for unexpected properties
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        errors.append(
            f"Unexpected key(s): {', '.join(sorted(unexpected))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required: name
    name = frontmatter.get("name", "").strip()
    if not name:
        errors.append("Missing 'name' in frontmatter")
    else:
        if not re.match(r"^[a-z0-9-]+$", name):
            errors.append(f"Name '{name}' must be kebab-case (lowercase letters, digits, hyphens)")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append(f"Name '{name}' cannot start/end with hyphen or have consecutive hyphens")
        if len(name) > 64:
            errors.append(f"Name too long ({len(name)} chars, max 64)")
        if name != skill_path.name:
            errors.append(f"Name '{name}' does not match directory '{skill_path.name}'")

    # Check required: description
    description = frontmatter.get("description", "").strip()
    if not description:
        errors.append("Missing 'description' in frontmatter")
    else:
        if "<" in description or ">" in description:
            errors.append("Description cannot contain angle brackets (< or >)")
        if len(description) > 1024:
            errors.append(f"Description too long ({len(description)} chars, max 1024)")

    # Check body exists
    body_match = re.match(r"^---\n.*?\n---\n?(.*)", content, re.DOTALL)
    body = body_match.group(1).strip() if body_match else ""
    if not body:
        errors.append("No body content after frontmatter")

    body_lines = body.count("\n") + 1 if body else 0
    if body_lines > 500:
        warnings.append(f"Body is {body_lines} lines (recommended max 500)")

    # Check optional: compatibility
    compat = frontmatter.get("compatibility", "").strip()
    if compat and len(compat) > 500:
        errors.append(f"Compatibility too long ({len(compat)} chars, max 500)")

    passed = len(errors) == 0
    return passed, errors, warnings


def main():
    skills_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills")

    if not skills_dir.is_dir():
        print(f"Error: '{skills_dir}' is not a directory")
        sys.exit(1)

    # Find all skill directories (contain SKILL.md)
    skill_dirs = sorted([d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()])

    if not skill_dirs:
        print(f"No skills found in '{skills_dir}' (looking for */SKILL.md)")
        sys.exit(1)

    total = len(skill_dirs)
    passed_count = 0
    failed_count = 0

    for skill_dir in skill_dirs:
        passed, errors, warnings = validate_skill(skill_dir)
        status = "PASS" if passed else "FAIL"

        if passed:
            passed_count += 1
            print(f"  [{status}] {skill_dir.name}")
        else:
            failed_count += 1
            print(f"  [{status}] {skill_dir.name}")

        for err in errors:
            print(f"         Error: {err}")
        for warn in warnings:
            print(f"         Warning: {warn}")

    print(f"\nResults: {passed_count}/{total} passed", end="")
    if failed_count:
        print(f", {failed_count} failed")
    else:
        print()

    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
