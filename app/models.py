from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import date

class Eligibility(BaseModel):
    allowedUserTiers: Optional[List[str]] = None
    minLifetimeSpend: Optional[float] = None
    minOrdersPlaced: Optional[int] = None
    firstOrderOnly: Optional[bool] = None
    allowedCountries: Optional[List[str]] = None

    minCartValue: Optional[float] = None
    applicableCategories: Optional[List[str]] = None
    excludedCategories: Optional[List[str]] = None
    minItemsCount: Optional[int] = None
    
class Coupon(BaseModel):
    code: str
    description: str
    discountType: Literal["FLAT", "PERCENT"]
    discountValue: float
    startDate: date
    endDate: date
    maxDiscountAmount: Optional[float] = None
    usageLimitPerUser: Optional[int] = None
    eligibility: Optional[Eligibility] = None


class UserContext(BaseModel):
    userId: str
    userTier: str
    country: str
    lifetimeSpend: float
    ordersPlaced: int


class CartItem(BaseModel):
    productId: str
    category: str
    unitPrice: float
    quantity: int

class Cart(BaseModel):
    items: List[CartItem]