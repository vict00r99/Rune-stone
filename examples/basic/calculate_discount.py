# Generated from: calculate_discount.rune


def calculate_discount(price: float, percentage: int) -> float:
    """
    Calculates the final price after applying a discount percentage.

    Args:
        price: Original price (must be non-negative).
        percentage: Discount percentage between 0 and 100.

    Returns:
        Discounted price rounded to 2 decimal places.

    Raises:
        ValueError: If price is negative or percentage is out of range.
    """
    if percentage < 0:
        raise ValueError("Discount percentage cannot be negative")
    if percentage > 100:
        raise ValueError("Discount percentage cannot exceed 100")
    if price < 0:
        raise ValueError("Price cannot be negative")

    discount_amount = price * (percentage / 100)
    final_price = price - discount_amount
    return round(final_price, 2)
