# Generated from: specs/check_free_shipping.rune

STANDARD_THRESHOLD = 50.00
PROMO_THRESHOLD = 30.00


def check_free_shipping(
    subtotal: float, is_loyalty_member: bool, is_promo_period: bool = False
) -> tuple[bool, str]:
    """
    Determines if an order qualifies for free shipping.

    Args:
        subtotal: Pre-tax order amount (must be non-negative).
        is_loyalty_member: Whether the customer is a loyalty program member.
        is_promo_period: Whether a promotional period is active (default False).

    Returns:
        Tuple of (eligible, reason) explaining the decision.

    Raises:
        ValueError: If subtotal is negative.
    """
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")

    if is_loyalty_member:
        return (True, "Loyalty program member")

    if is_promo_period and subtotal >= PROMO_THRESHOLD:
        return (True, "Promotional free shipping")

    if not is_promo_period and subtotal >= STANDARD_THRESHOLD:
        return (True, "Order over $50")

    return (False, "Minimum not met")
