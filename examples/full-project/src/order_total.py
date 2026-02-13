# Generated from: specs/calculate_order_total.rune


def calculate_order_total(items: list[dict], tax_rate: float) -> float:
    """
    Calculates the total cost of a bookstore order including tax.

    Args:
        items: List of dicts, each with 'price' (float > 0) and 'quantity' (int > 0).
        tax_rate: Tax percentage between 0 and 25.

    Returns:
        Total price rounded to 2 decimal places.

    Raises:
        ValueError: If price/quantity are not positive or tax_rate is out of range.
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    if tax_rate > 25:
        raise ValueError("Tax rate cannot exceed 25%")

    if not items:
        return 0.00

    subtotal = 0.0
    for item in items:
        price = item["price"]
        quantity = item["quantity"]

        if price <= 0:
            raise ValueError("Item price must be positive")
        if quantity <= 0:
            raise ValueError("Item quantity must be positive")

        subtotal += price * quantity

    tax = subtotal * (tax_rate / 100)
    total = subtotal + tax
    return round(total, 2)
