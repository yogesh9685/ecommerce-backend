from fastapi import APIRouter

from app.api.v1 import (
    auth, users, addresses, products, categories,
    brands, search, cart, wishlist, coupons,
    orders, payments, reviews, uploads, notifications, admin
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(addresses.router)
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(brands.router)
api_router.include_router(search.router)
api_router.include_router(cart.router)
api_router.include_router(wishlist.router)
api_router.include_router(coupons.router)
api_router.include_router(orders.router)
api_router.include_router(payments.router)
api_router.include_router(reviews.router)
api_router.include_router(uploads.router)
api_router.include_router(notifications.router)
api_router.include_router(admin.router)
