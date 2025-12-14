# Coupon Management System

## Project Overview

This project is a simple backend coupon management system built as an HTTP API.
It allows creating coupons with eligibility rules and selecting the best applicable coupon for a given user and cart based on defined business logic.

The system evaluates coupons deterministically using eligibility rules, discount calculations, and tie-breakers.

## Tech Stack

Language: Python 3.10+

Framework: FastAPI

Validation: Pydantic

Storage: In-memory (Python list)

Server: Uvicorn

## Features

Create coupons with user-based and cart-based eligibility rules

Supports FLAT and PERCENT discounts

Applies max discount caps for percentage coupons

Selects the best coupon using:

Highest discount

Earliest expiry date

Lexicographical coupon code

No database required (as per assignment)

API Endpoints
1️⃣ Create Coupon

POST /coupons

Creates and stores a coupon in memory.
Duplicate coupon codes are rejected.

Sample Request

{
  "code": "WELCOME100",
  "description": "₹100 off for new users",
  "discountType": "FLAT",
  "discountValue": 100,
  "startDate": "2025-01-01",
  "endDate": "2025-12-31",
  "eligibility": {
    "firstOrderOnly": true
  }
}

2️⃣ Get Best Coupon

POST /coupons/best

Returns the best applicable coupon for a given user and cart.

Sample Request

{
  "user": {
    "userId": "u1",
    "userTier": "NEW",
    "country": "IN",
    "lifetimeSpend": 0,
    "ordersPlaced": 0
  },
  "cart": {
    "items": [
      {
        "productId": "p1",
        "category": "electronics",
        "unitPrice": 1500,
        "quantity": 1
      }
    ]
  }
}


 Sample Response

{
  "coupon": {
    "code": "ELEC10",
    "description": "10% off electronics",
    "discountType": "PERCENT",
    "discountValue": 10,
    "startDate": "2025-01-01",
    "endDate": "2025-12-31"
  },
  "discount": 150.0
}

## Eligibility Rules Supported
User-based

allowedUserTiers
minLifetimeSpend
minOrdersPlaced
firstOrderOnly
allowedCountries

Cart-based

minCartValue
minItemsCount
applicableCategories

excludedCategories

If a rule is not provided, it is ignored.

How to Run
Prerequisites

Python 3.10+

Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Run Server
uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000/docs

## Design Decisions

Used in-memory storage as allowed by the assignment

No authentication or database to keep focus on business logic

Eligibility rules evaluated independently with early failure

Usage limit is checked logically but not persisted (redemption out of scope)

AI Usage Note

AI was used as a learning assistant to:

Understand assignment requirements

Improve logic structure

Review and validate business logic

All implementation decisions and code were written and understood by the author.

Author

Role: Backend Developer
Assignment: Coupon Management System