"""
Models package — import all models here so SQLAlchemy and Alembic
can discover them via Base.metadata.
"""
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.address import Address
from app.models.category import Category
from app.models.brand import Brand
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.product_variant import ProductVariant
from app.models.inventory import Inventory
from app.models.cart import CartItem
from app.models.wishlist import WishlistItem
from app.models.coupon import Coupon
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.review import Review
from app.models.otp import OTP
from app.models.session import Session
from app.models.audit_log import AuditLog

__all__ = [
    "User", "Role", "Permission", "Address",
    "Category", "Brand", "Product", "ProductImage", "ProductVariant", "Inventory",
    "CartItem", "WishlistItem", "Coupon",
    "Order", "OrderItem", "Payment", "Review",
    "OTP", "Session", "AuditLog",
]
