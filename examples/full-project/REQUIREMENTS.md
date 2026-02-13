# Online Bookstore - Order Processing

## Context

We're building the order processing module for an online bookstore. Customers browse books, add them to a cart, apply coupon codes, and check out. We need three core functions for the checkout flow.

## Business Rules

### 1. Calculate Order Total

The system must calculate the total cost of an order including tax.

- Each item in the cart has a **price** (in USD) and a **quantity**
- A **tax rate** is applied to the subtotal (varies by state, passed as parameter)
- The subtotal is the sum of (price x quantity) for all items
- The total is subtotal + tax, rounded to 2 decimal places
- An empty cart should return 0.00
- Prices and quantities must be positive numbers
- Tax rate is a percentage between 0% and 25%

**Example:** 2 books at $15.99 + 1 book at $24.50 with 8.5% tax = $61.28

### 2. Validate Coupon

The system must validate coupon codes and return the discount they provide.

- Coupons have a **code** (string), a **discount type** ("percentage" or "fixed"), a **discount value**, and an **expiration date**
- The function receives the coupon code and a list of active coupons
- It must check: does the code exist? has it expired? is the format valid?
- Returns the matching coupon data if valid, or an error message if not
- Coupon codes are case-insensitive (SAVE10 = save10)
- Expired coupons must be rejected even if the code is correct

**Example:** Code "SAVE10" → matches coupon with 10% discount, not expired → valid

### 3. Check Free Shipping Eligibility

The system must determine if an order qualifies for free shipping.

- Orders over $50 (subtotal, before tax) get free shipping
- Members of the loyalty program always get free shipping regardless of amount
- During promotional periods (a boolean flag), the threshold drops to $30
- Returns True/False and the reason
- The subtotal must be a non-negative number

**Example:** Subtotal $45, loyalty member → free shipping (loyalty program)

## Acceptance Criteria

- All functions must have proper input validation
- Errors must be descriptive (not generic "invalid input")
- Monetary values must be rounded to 2 decimal places
- All edge cases must be handled (empty inputs, zero values, boundary values)
