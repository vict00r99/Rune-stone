# Generated from: validate_email.rune

import re

EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)


def validate_email(email: str) -> tuple[bool, str]:
    """
    Validates an email address against RFC 5322 standards.

    Args:
        email: The email address string to validate.

    Returns:
        Tuple of (is_valid, message) where message explains the result.
    """
    if not email:
        return (False, "Email cannot be empty")

    if len(email) > 254:
        return (False, "Email exceeds maximum length of 254 characters")

    if email.count("@") == 0:
        return (False, "Missing @ symbol")

    if email.count("@") > 1:
        return (False, "Multiple @ symbols not allowed")

    local, domain = email.split("@")

    if not local:
        return (False, "Local part cannot be empty")

    if len(local) > 64:
        return (False, "Local part exceeds maximum length of 64 characters")

    if not domain:
        return (False, "Domain cannot be empty")

    if len(domain) > 253:
        return (False, "Domain exceeds maximum length of 253 characters")

    if "." not in domain:
        return (False, "Domain must have at least one dot")

    if " " in email:
        return (False, "Invalid email format")

    if EMAIL_PATTERN.match(email):
        return (True, "Valid email")

    return (False, "Invalid email format")
