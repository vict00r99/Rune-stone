# Generated from: ../slugify.rune

import re
import unicodedata


def slugify(text: str, separator: str = "-") -> str:
    """
    Converts a text string into a URL-friendly slug.

    Args:
        text: Any string to slugify.
        separator: Character to join words (default: hyphen).

    Returns:
        Lowercase slug with only [a-z0-9] and the separator.
    """
    if not text:
        return ""

    # Normalize unicode and decompose accented characters
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")

    # Lowercase
    slug = ascii_text.lower()

    # Remove everything that's not alphanumeric, space, or hyphen
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)

    # Replace whitespace and hyphens with separator
    slug = re.sub(r"[\s-]+", separator, slug)

    # Trim leading/trailing separators
    slug = slug.strip(separator)

    return slug
