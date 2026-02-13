# Tests generated from: specs/check_free_shipping.rune

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from shipping import check_free_shipping


class TestLoyaltyMember:
    def test_loyalty_small_order(self):
        assert check_free_shipping(10.00, True) == (True, "Loyalty program member")

    def test_loyalty_zero_order(self):
        assert check_free_shipping(0.00, True) == (True, "Loyalty program member")

    def test_loyalty_overrides_promo(self):
        assert check_free_shipping(10.00, True, True) == (
            True,
            "Loyalty program member",
        )


class TestStandardThreshold:
    def test_at_threshold(self):
        assert check_free_shipping(50.00, False) == (True, "Order over $50")

    def test_above_threshold(self):
        assert check_free_shipping(75.00, False) == (True, "Order over $50")

    def test_below_threshold(self):
        assert check_free_shipping(49.99, False) == (False, "Minimum not met")


class TestPromoThreshold:
    def test_at_promo_threshold(self):
        assert check_free_shipping(30.00, False, True) == (
            True,
            "Promotional free shipping",
        )

    def test_above_promo_threshold(self):
        assert check_free_shipping(45.00, False, True) == (
            True,
            "Promotional free shipping",
        )

    def test_below_promo_threshold(self):
        assert check_free_shipping(29.99, False, True) == (False, "Minimum not met")


class TestEdgeCases:
    def test_zero_not_member(self):
        assert check_free_shipping(0.00, False) == (False, "Minimum not met")

    def test_negative_subtotal(self):
        with pytest.raises(ValueError, match="Subtotal cannot be negative"):
            check_free_shipping(-1.00, False)
