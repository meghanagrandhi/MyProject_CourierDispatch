"""Lab 6 - test cases for BRANCH coverage of shopping_cart.py.

Every decision in shopping_cart.py is exercised both ways (True and False),
with boundary values for each condition.

Run:
    coverage run --branch -m pytest BranchCoverageTest_shopping_cart_application.py
    coverage report -m
"""
import pytest
from shopping_cart import item_total, cart_discount, shipping_fee


# ---------------------------------------------------------------- item_total
# Example test cases given in the starter file
def test_food_item():
    assert item_total("food", 100, 2) == 210


def test_free_shipping():
    assert shipping_fee(1000, False, False) == 0


# Every category in GST_RATE
def test_electronics_item():
    assert item_total("electronics", 1000, 1) == 1180


def test_clothing_item():
    assert item_total("clothing", 500, 1) == 560


# Bulk discount branch: qty >= 10 (True) and qty < 10 (False), with boundaries
def test_bulk_discount_at_ten():
    # 10 x 100 = 1000, minus 10% = 900, plus 5% GST = 945
    assert item_total("food", 100, 10) == 945


def test_bulk_discount_above_ten():
    # 11 x 100 = 1100, minus 110 = 990, plus 990*5//100 = 49
    assert item_total("food", 100, 11) == 1039


def test_no_bulk_discount_at_nine():
    # 9 x 100 = 900 with no discount, plus 45 GST
    assert item_total("food", 100, 9) == 945 and item_total("clothing", 100, 9) == 1008


def test_integer_division_truncates_gst():
    # 33 + (33 * 5 // 100 = 1) = 34
    assert item_total("food", 33, 1) == 34


def test_zero_price_is_allowed():
    assert item_total("food", 0, 3) == 0


# Error branches: each part of "price < 0 or qty <= 0" on its own
def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        item_total("toys", 100, 1)


def test_negative_price_raises():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -1, 1)


def test_zero_quantity_raises():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, 0)


def test_negative_quantity_raises():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, -5)


# ------------------------------------------------------------- cart_discount
# Tier branches (>= 5000, >= 2000, else) with boundary values
@pytest.mark.parametrize("value, expected", [
    (6000, 500),
    (5000, 500),
    (4999, 200),
    (2000, 200),
    (1999, 0),
    (0, 0),
])
def test_cart_discount_tiers(value, expected):
    assert cart_discount(value, False, None) == expected


# Prime branch (True and False)
def test_prime_adds_100():
    assert cart_discount(1000, True, None) == 100


def test_prime_with_top_tier():
    assert cart_discount(5000, True, None) == 600


# Coupon branch: coupon matches / does not match, value >= 1000 / below
def test_flat10_coupon_applied_at_1000():
    assert cart_discount(1000, False, "FLAT10") == 100


def test_flat10_coupon_not_applied_below_1000():
    assert cart_discount(999, False, "FLAT10") == 0


def test_wrong_coupon_code_ignored():
    assert cart_discount(1000, False, "SAVE20") == 0


def test_all_discounts_together():
    # 500 (tier) + 100 (prime) + 500 (FLAT10 on 5000)
    assert cart_discount(5000, True, "FLAT10") == 1100


def test_flat10_with_mid_tier():
    # 200 (tier) + 200 (FLAT10 on 2000)
    assert cart_discount(2000, False, "FLAT10") == 400


# -------------------------------------------------------------- shipping_fee
def test_standard_shipping_below_500():
    assert shipping_fee(499, False, False) == 40


def test_free_shipping_at_500():
    assert shipping_fee(500, False, False) == 0


def test_prime_always_free_standard_shipping():
    assert shipping_fee(100, True, False) == 0


def test_express_non_prime_below_500():
    assert shipping_fee(100, False, True) == 140


def test_express_non_prime_free_threshold():
    assert shipping_fee(500, False, True) == 100


def test_express_prime_gets_50_off():
    assert shipping_fee(100, True, True) == 50


def test_express_prime_large_cart():
    assert shipping_fee(1000, True, True) == 50
