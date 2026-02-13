# Generated from: specs/validate_coupon.rune


def validate_coupon(
    code: str, active_coupons: list[dict], current_date: str
) -> tuple[bool, dict | str]:
    """
    Validates a coupon code against a list of active coupons.

    Args:
        code: Coupon code string (case-insensitive comparison).
        active_coupons: List of coupon dicts with keys:
            'code', 'discount_type', 'discount_value', 'expires_at'.
        current_date: ISO 8601 date string (YYYY-MM-DD).

    Returns:
        (True, coupon_data) if valid, or (False, error_message) if not.
    """
    if not code:
        return (False, "Coupon code cannot be empty")

    code_upper = code.upper()

    match = None
    for coupon in active_coupons:
        if coupon["code"].upper() == code_upper:
            match = coupon
            break

    if match is None:
        return (False, "Coupon code not found")

    if match["expires_at"] < current_date:
        return (False, "Coupon has expired")

    discount_type = match.get("discount_type")
    discount_value = match.get("discount_value", 0)

    if discount_type not in ("percentage", "fixed"):
        return (False, "Invalid coupon configuration")

    if discount_type == "percentage" and (discount_value <= 0 or discount_value > 100):
        return (False, "Invalid discount value")

    if discount_type == "fixed" and discount_value <= 0:
        return (False, "Invalid discount value")

    return (True, match)
