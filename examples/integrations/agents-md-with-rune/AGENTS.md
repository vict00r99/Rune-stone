# AGENTS.md — Online Bookstore

## Project Context

- **Language:** Python 3.11
- **Framework:** FastAPI
- **Testing:** pytest
- **Architecture:** Service layer with dependency injection

## Conventions

- All monetary values as `float`, rounded to 2 decimal places
- All dates as ISO 8601 strings (`YYYY-MM-DD`)
- Error messages must be specific (never generic "invalid input")
- All public functions must have type hints and docstrings

## Function Specifications

The following specs define the contracts for the order processing module.

---

### calculate_order_total

**SIGNATURE:** `def calculate_order_total(items: list[dict], tax_rate: float) -> float`

**INTENT:** Calculates the total cost of an order including tax. Each item has a price and quantity. Returns the final total rounded to 2 decimal places.

**BEHAVIOR:**
- WHEN items is empty THEN return 0.00
- WHEN any item has price <= 0 THEN raise ValueError("Item price must be positive")
- WHEN any item has quantity <= 0 THEN raise ValueError("Item quantity must be positive")
- WHEN tax_rate < 0 THEN raise ValueError("Tax rate cannot be negative")
- WHEN tax_rate > 25 THEN raise ValueError("Tax rate cannot exceed 25%")
- CALCULATE subtotal = sum of (price * quantity) for each item
- CALCULATE total = subtotal + (subtotal * tax_rate / 100)
- RETURN round(total, 2)

**TESTS:**
- `calculate_order_total([{'price': 15.99, 'quantity': 2}, {'price': 24.50, 'quantity': 1}], 8.5) == 61.28`
- `calculate_order_total([], 8.5) == 0.00`
- `calculate_order_total([{'price': 100.0, 'quantity': 1}], 0) == 100.00`
- `calculate_order_total([{'price': -5.0, 'quantity': 1}], 8.5) raises ValueError`
- `calculate_order_total([{'price': 10.0, 'quantity': 0}], 8.5) raises ValueError`

**EDGE_CASES:**
- Empty cart: returns 0.00
- Zero tax: total equals subtotal
- Single item with quantity 1: total equals price + tax

---

### validate_coupon

**SIGNATURE:** `def validate_coupon(code: str, active_coupons: list[dict], current_date: str) -> tuple[bool, dict | str]`

**INTENT:** Validates a coupon code against active coupons. Case-insensitive matching. Returns (True, coupon_data) if valid, (False, error_message) if not.

**BEHAVIOR:**
- WHEN code is empty THEN return (False, "Coupon code cannot be empty")
- WHEN code not found (case-insensitive) THEN return (False, "Coupon code not found")
- WHEN matching coupon has expired THEN return (False, "Coupon has expired")
- WHEN discount value is invalid THEN return (False, "Invalid discount value")
- OTHERWISE return (True, matching_coupon)

**TESTS:**
- `validate_coupon('SAVE10', [coupon_save10], '2025-01-15')[0] == True`
- `validate_coupon('save10', [coupon_save10], '2025-01-15')[0] == True` (case-insensitive)
- `validate_coupon('INVALID', [coupon_save10], '2025-01-15')[0] == False`
- `validate_coupon('OLD', [expired_coupon], '2025-01-15')[0] == False`
- `validate_coupon('', [], '2025-01-15')[0] == False`

**EDGE_CASES:**
- Case mismatch (SAVE10 vs save10): should match
- Expires today: still valid
- Empty coupons list: returns "not found"

---

### check_free_shipping

**SIGNATURE:** `def check_free_shipping(subtotal: float, is_loyalty_member: bool, is_promo_period: bool = False) -> tuple[bool, str]`

**INTENT:** Determines if an order qualifies for free shipping based on subtotal, loyalty status, and promotional period.

**BEHAVIOR:**
- WHEN subtotal < 0 THEN raise ValueError("Subtotal cannot be negative")
- WHEN is_loyalty_member is True THEN return (True, "Loyalty program member")
- WHEN is_promo_period is True AND subtotal >= 30 THEN return (True, "Promotional free shipping")
- WHEN subtotal >= 50 THEN return (True, "Order over $50")
- OTHERWISE return (False, "Minimum not met")

**TESTS:**
- `check_free_shipping(10.00, True) == (True, "Loyalty program member")`
- `check_free_shipping(50.00, False) == (True, "Order over $50")`
- `check_free_shipping(49.99, False) == (False, "Minimum not met")`
- `check_free_shipping(30.00, False, True) == (True, "Promotional free shipping")`
- `check_free_shipping(-1.00, False) raises ValueError`

**EDGE_CASES:**
- Loyalty member with $0 order: still eligible
- Exactly at $50 threshold: eligible
- Promo period with $29.99: not eligible
