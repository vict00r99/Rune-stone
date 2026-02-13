# Tests generated from: specs/validate_coupon.rune

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from coupon import validate_coupon

SAVE10 = {
    "code": "SAVE10",
    "discount_type": "percentage",
    "discount_value": 10,
    "expires_at": "2099-12-31",
}
FLAT5 = {
    "code": "FLAT5",
    "discount_type": "fixed",
    "discount_value": 5.00,
    "expires_at": "2099-12-31",
}
EXPIRED = {
    "code": "OLD",
    "discount_type": "percentage",
    "discount_value": 10,
    "expires_at": "2020-01-01",
}
EXPIRES_TODAY = {
    "code": "TODAY",
    "discount_type": "percentage",
    "discount_value": 10,
    "expires_at": "2025-01-15",
}
BAD_VALUE = {
    "code": "BAD",
    "discount_type": "percentage",
    "discount_value": 150,
    "expires_at": "2099-12-31",
}


class TestValidCoupon:
    def test_percentage_coupon(self):
        valid, result = validate_coupon("SAVE10", [SAVE10], "2025-01-15")
        assert valid is True
        assert result["discount_value"] == 10

    def test_fixed_coupon(self):
        valid, result = validate_coupon("FLAT5", [FLAT5], "2025-01-15")
        assert valid is True
        assert result["discount_type"] == "fixed"

    def test_case_insensitive(self):
        valid, _ = validate_coupon("save10", [SAVE10], "2025-01-15")
        assert valid is True

    def test_expires_today_still_valid(self):
        valid, _ = validate_coupon("TODAY", [EXPIRES_TODAY], "2025-01-15")
        assert valid is True


class TestInvalidCoupon:
    def test_not_found(self):
        valid, msg = validate_coupon("INVALID", [SAVE10], "2025-01-15")
        assert valid is False
        assert msg == "Coupon code not found"

    def test_expired(self):
        valid, msg = validate_coupon("OLD", [EXPIRED], "2025-01-15")
        assert valid is False
        assert msg == "Coupon has expired"

    def test_empty_code(self):
        valid, msg = validate_coupon("", [], "2025-01-15")
        assert valid is False
        assert msg == "Coupon code cannot be empty"

    def test_empty_coupons_list(self):
        valid, msg = validate_coupon("SAVE10", [], "2025-01-15")
        assert valid is False
        assert msg == "Coupon code not found"

    def test_invalid_discount_value(self):
        valid, msg = validate_coupon("BAD", [BAD_VALUE], "2025-01-15")
        assert valid is False
        assert msg == "Invalid discount value"
