from typing import List, Optional
from datetime import date
from app.models import Cart, Coupon, Eligibility, UserContext

def calculate_cart_value(cart: Cart) -> float:
    total = 0.0
    for item in cart.items:
        total += item.unitPrice * item.quantity
    return total

def calculate_item_count(cart: Cart) -> int:
    total = 0
    for item in cart.items:
        total += item.quantity
    return total

def is_coupon_valid_today(coupon: Coupon) -> bool:
    today = date.today()
    return coupon.startDate <= today <= coupon.endDate

def is_user_eligible(eligibility: Eligibility,user: UserContext) -> bool:
    if eligibility == None:
        return True
    if eligibility.allowedUserTiers is not None:
        if user.userTier not in eligibility.allowedUserTiers:
            return False
    if eligibility.minLifetimeSpend is not None:
        if user.lifetimeSpend < eligibility.minLifetimeSpend:
            return False
    if eligibility.minOrdersPlaced is not None:
        if user.ordersPlaced < eligibility.minOrdersPlaced:
            return False
    if eligibility.firstOrderOnly is True:
        if user.ordersPlaced != 0:
            return False
    if eligibility.allowedCountries is not None:
        if user.country not in eligibility.allowedCountries:
            return False
    return True

def is_cart_eligible(eligibility: Eligibility, cart: Cart) -> bool:
    if eligibility is None:
        return True
    if eligibility.minCartValue is not None:
        if calculate_cart_value(cart) < eligibility.minCartValue:
            return False
    if eligibility.minItemsCount is not None:
        if calculate_item_count(cart) < eligibility.minItemsCount:
            return False
    if eligibility.applicableCategories is not None:
        cart_categories = {item.category for item in cart.items}
        if not any(cat in cart_categories for cat in eligibility.applicableCategories):
            return False
    if eligibility.excludedCategories is not None:
        for item in cart.items:
            if item.category in eligibility.excludedCategories:
                return False
    return True

def calculate_discount(coupon: Coupon, cart: Cart) -> float:
    cart_value = calculate_cart_value(cart)
    if coupon.discountType == "FLAT":
        discount = coupon.discountValue
    elif coupon.discountType == "PERCENT":
        discount = (coupon.discountValue / 100) * cart_value
    if coupon.maxDiscountAmount is not None:
        discount = min(discount, coupon.maxDiscountAmount)
    else:
        discount = 0.0
    return min(discount, cart_value)

def select_best_coupon(
    coupons: List[Coupon],
    user: UserContext,
    cart: Cart
) -> tuple[Optional[Coupon], float]:

    best_coupon: Optional[Coupon] = None
    best_discount: float = 0.0

    for coupon in coupons:
        if not is_coupon_valid_today(coupon):
            continue

        if not is_user_eligible(coupon.eligibility, user):
            continue

        if not is_cart_eligible(coupon.eligibility, cart):
            continue

        discount = calculate_discount(coupon, cart)

        if discount <= 0:
            continue

        if discount > best_discount:
            best_coupon = coupon
            best_discount = discount

        elif discount == best_discount and best_coupon is not None:
            if coupon.endDate < best_coupon.endDate:
                best_coupon = coupon
            elif coupon.endDate == best_coupon.endDate:
                if coupon.code < best_coupon.code:
                    best_coupon = coupon

    return best_coupon, best_discount

