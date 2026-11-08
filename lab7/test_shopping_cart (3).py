"""Lab 7: fuzz tests for shopping_cart.py using Hypothesis.

Two kinds of properties are checked:
  1. Robustness: no input at all may crash a function (it must not raise).
  2. Correctness: well-formed inputs give exactly the expected answer, and
     malformed inputs give None instead of an exception or a wrong number.
"""
from hypothesis import given, example, strategies as st
from shopping_cart import cart_total, promo_percent, delivery_zone, ZONES

# Hostile inputs of many types, not just text
anything = st.one_of(
    st.none(), st.text(), st.integers(), st.floats(), st.binary(),
    st.lists(st.text()),
)


# ------------------------------------------------------------ no-crash fuzz
@given(st.text() | st.none())
@example("pen:10")            # missing 'x'
@example("")                  # empty cart
@example("a:1x1,,b:2x2")      # empty item
@example("a:-5x2")            # negative price
@example("a:1x0")             # zero quantity
@example("a:1²x1")            # non-ASCII digit
@example("a:" + "9" * 5000 + "x1")   # absurdly long number
@example(None)
def test_cart_total_no_crash(s):
    try:
        cart_total(s)
    except Exception as e:
        assert False, f"cart_total crashed with: {e!r}"


@given(st.text() | st.none())
@example("")
@example("OFF")               # no number
@example("OFFabc")            # not a number
@example("NOCODE")            # no OFF at all
@example("OFF-5")             # negative
@example("OFF500")            # over 100 percent
@example("OFF20OFF30")        # two OFFs
@example(None)
def test_promo_percent_no_crash(s):
    try:
        promo_percent(s)
    except Exception as e:
        assert False, f"promo_percent crashed with: {e!r}"


@given(st.text() | st.none())
@example("")                  # empty pincode
@example("0")                 # first digit not in ZONES
@example("912345")
@example("abcdef")
@example("56008")             # too short
@example("5600850")           # too long
@example(None)
def test_delivery_zone_no_crash(s):
    try:
        delivery_zone(s)
    except Exception as e:
        assert False, f"delivery_zone crashed with: {e!r}"


# Same robustness check with non-string inputs (ints, floats, bytes, lists)
@given(anything)
def test_no_function_crashes_on_any_type(x):
    for func in (cart_total, promo_percent, delivery_zone):
        try:
            func(x)
        except Exception as e:
            assert False, f"{func.__name__} crashed on {x!r} with: {e!r}"


# ------------------------------------------------------ correctness fuzzing
names = st.text(alphabet="abcxyzXYZ _-", min_size=1).filter(lambda n: n.strip())
items = st.tuples(names, st.integers(0, 10**6), st.integers(1, 1000))


@given(st.lists(items, min_size=1, max_size=10))
def test_cart_total_matches_sum_for_valid_carts(cart):
    text = ",".join(f"{n}:{p}x{q}" for n, p, q in cart)
    assert cart_total(text) == sum(p * q for _, p, q in cart)


@given(st.text() | st.none())
def test_cart_total_returns_non_negative_int_or_none(s):
    result = cart_total(s)
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.integers(0, 100), st.sampled_from(["OFF", "off", "Off", "SAVEOFF"]))
def test_promo_percent_valid_codes(n, prefix):
    assert promo_percent(f"{prefix}{n}") == n


@given(st.integers(101, 9999))
def test_promo_percent_rejects_over_100(n):
    assert promo_percent(f"OFF{n}") is None


@given(st.text() | st.none())
def test_promo_percent_result_is_0_to_100_or_none(s):
    result = promo_percent(s)
    assert result is None or (isinstance(result, int) and 0 <= result <= 100)


@given(st.sampled_from(sorted(ZONES)), st.integers(0, 99999))
def test_delivery_zone_valid_pincodes(first, rest):
    pincode = first + f"{rest:05d}"
    assert delivery_zone(pincode) == ZONES[first]


@given(st.sampled_from("09"), st.integers(0, 99999))
def test_delivery_zone_rejects_unserved_first_digit(first, rest):
    assert delivery_zone(first + f"{rest:05d}") is None


@given(st.text() | st.none())
def test_delivery_zone_result_is_known_zone_or_none(s):
    assert delivery_zone(s) in set(ZONES.values()) | {None}
