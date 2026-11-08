import re

ZONES = {"1": "North", "2": "North", "3": "West", "4": "West",
         "5": "South", "6": "South", "7": "East", "8": "East"}

# One cart item: name:pricexqty  (price and qty are plain ASCII digits, max 9)
_ITEM = re.compile(r"([^:,]+):([0-9]{1,9})x([0-9]{1,9})")
# Promo code: optional letters, then OFF, then a 1-3 digit percentage
_PROMO = re.compile(r"[A-Z]*OFF([0-9]{1,3})")
# Pincode: exactly 6 ASCII digits
_PINCODE = re.compile(r"[0-9]{6}")


def cart_total(cart):
    """Total of a 'name:pricexqty,name:pricexqty' cart.

    Returns the total as an int, or None if the cart is not valid
    (not a string, empty, empty item, missing ':' or 'x', negative or
    non-ASCII numbers, numbers longer than 9 digits, quantity of 0).
    """
    if not isinstance(cart, str) or not cart.strip():
        return None
    total = 0
    for item in cart.split(','):
        match = _ITEM.fullmatch(item.strip())
        if match is None or not match.group(1).strip():
            return None
        price, qty = int(match.group(2)), int(match.group(3))
        if qty < 1:
            return None
        total += price * qty
    return total


def promo_percent(code):
    """Discount percentage (0-100) from a code like 'OFF20'.

    Returns None if the code is not a string, is not ASCII, does not match
    the pattern, or the percentage is above 100.
    """
    if not isinstance(code, str) or not code.isascii():
        return None
    match = _PROMO.fullmatch(code.strip().upper())
    if match is None:
        return None
    percent = int(match.group(1))
    return percent if percent <= 100 else None


def delivery_zone(pincode):
    """Delivery zone for a 6-digit pincode.

    Returns the zone name, or None if the pincode is not a string of exactly
    6 ASCII digits or its first digit is not served.
    """
    if not isinstance(pincode, str):
        return None
    pincode = pincode.strip()
    if _PINCODE.fullmatch(pincode) is None:
        return None
    return ZONES.get(pincode[0])


def main():
    print("==== Running cart_total ====")
    user_input = input("Enter cart as name:pricexqty CSV (e.g. pen:10x2,book:250x1): ")
    result = cart_total(user_input)
    print("Cart Total:", result if result is not None else "Invalid cart")

    print("\n==== Running promo_percent ====")
    user_input = input("Enter a promo code (e.g. OFF20): ")
    result = promo_percent(user_input)
    print("Discount Percent:", result if result is not None else "Invalid promo code")

    print("\n==== Running delivery_zone ====")
    user_input = input("Enter a 6 digit pincode (e.g. 560085): ")
    result = delivery_zone(user_input)
    print("Delivery Zone:", result if result is not None else "Invalid or unserved pincode")


if __name__ == "__main__":
    main()
