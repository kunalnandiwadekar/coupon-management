from fastapi import FastAPI, HTTPException
from typing import List
from app.models import Coupon, UserContext, Cart
from app.logic import select_best_coupon
from pydantic import BaseModel

app = FastAPI(title="Coupon Management API")


@app.get("/")
def root():
    return {"status": "success",
            "message": "Welcome to Coupon Management API"
            }

# memory coupon storage
COUPONS: List[Coupon] = []

@app.post("/coupons")
def create_coupon(coupon: Coupon):
    # Check for duplicate coupon code
    for existing_coupon in COUPONS:
        if existing_coupon.code == coupon.code:
            raise HTTPException(
                status_code=400,
                detail=f"Coupon with code '{coupon.code}' already exists"
            )

    # Store coupon in memory
    COUPONS.append(coupon)

    return {
        "status": "success",
        "message": "Coupon created successfully",
        "code": coupon.code
    }


class BestCouponRequest(BaseModel):
    user: UserContext
    cart: Cart


@app.post("/coupons/best")
def get_best_coupon(payload: BestCouponRequest):
    if not COUPONS:
        return {
            "coupon": None,
            "discount": 0.0
        }

    best_coupon, best_discount = select_best_coupon(
        coupons=COUPONS,
        user=payload.user,
        cart=payload.cart
    )

    if best_coupon is None:
        return {
            "coupon": None,
            "discount": 0.0
        }

    return {
        "coupon": best_coupon,
        "discount": best_discount
    }
