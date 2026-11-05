"""Lab 6 - test cases for LINE (code) coverage of shopping_cart.py.

Run:
    coverage run -m pytest CodeCoverageTest_shopping_cart_application.py
    coverage report -m
"""
import pytest
from shopping_cart import item_total, cart_discount, shipping_fee


# ---------------------------------------------------------------- item_total
def test_food_item():
    assert item_total("food", 100, 2) == 210


def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        item_total("toys", 100, 1)


def test_invalid_price_raises():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -1, 1)


def test_bulk_discount_applied():
    # 10 x 100 = 1000, minus 10% = 900, plus 18% GST = 1062
    assert item_total("electronics", 100, 10) == 1062


# ------------------------------------------------------------- cart_discount
def test_top_tier_prime_and_coupon():
    # 500 (tier) + 100 (prime) + 600 (FLAT10 on 6000)
    assert cart_discount(6000, True, "FLAT10") == 1200


def test_mid_tier_discount():
    assert cart_discount(2500, False, None) == 200


def test_no_discount():
    assert cart_discount(100, False, None) == 0


# -------------------------------------------------------------- shipping_fee
def test_free_shipping_over_500():
    assert shipping_fee(1000, False, False) == 0


def test_standard_fee_with_express():
    # 40 standard + 100 express
    assert shipping_fee(100, False, True) == 140


def test_prime_express_discount():
    # prime: 0 + 100 express - 50
    assert shipping_fee(100, True, True) == 50
