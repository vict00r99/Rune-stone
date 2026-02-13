# Tests generated from: specs/calculate_order_total.rune

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from order_total import calculate_order_total


# Happy path
class TestHappyPath:
    def test_multiple_items_with_tax(self):
        items = [{"price": 15.99, "quantity": 2}, {"price": 24.50, "quantity": 1}]
        assert calculate_order_total(items, 8.5) == 61.28

    def test_single_item(self):
        assert calculate_order_total([{"price": 10.00, "quantity": 1}], 10.0) == 11.00

    def test_same_item_multiple_quantity(self):
        assert calculate_order_total([{"price": 9.99, "quantity": 3}], 7.0) == 32.07


# Empty cart
class TestEmptyCart:
    def test_empty_list(self):
        assert calculate_order_total([], 8.5) == 0.00


# Zero tax
class TestZeroTax:
    def test_no_tax(self):
        assert calculate_order_total([{"price": 25.00, "quantity": 2}], 0) == 50.00


# Boundary tax rate
class TestBoundaryTax:
    def test_max_tax(self):
        assert calculate_order_total([{"price": 100.00, "quantity": 1}], 25) == 125.00


# Rounding
class TestRounding:
    def test_complex_rounding(self):
        assert calculate_order_total([{"price": 33.33, "quantity": 3}], 8.875) == 108.86


# Error cases
class TestErrors:
    def test_negative_price(self):
        with pytest.raises(ValueError, match="Item price must be positive"):
            calculate_order_total([{"price": -5.00, "quantity": 1}], 8.5)

    def test_zero_quantity(self):
        with pytest.raises(ValueError, match="Item quantity must be positive"):
            calculate_order_total([{"price": 10.00, "quantity": 0}], 8.5)

    def test_negative_tax(self):
        with pytest.raises(ValueError, match="Tax rate cannot be negative"):
            calculate_order_total([{"price": 10.00, "quantity": 1}], -1)

    def test_excessive_tax(self):
        with pytest.raises(ValueError, match="Tax rate cannot exceed 25%"):
            calculate_order_total([{"price": 10.00, "quantity": 1}], 30)
