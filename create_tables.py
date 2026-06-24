"""
create_tables.py
----------------
Run this script to create all database tables from SQLAlchemy models.

Usage:
    # Option 1 — run directly
    python create_tables.py

    # Option 2 — inside IPython
    %run create_tables.py

    # Option 3 — paste into IPython manually (see below)
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# ── Import Base and ALL models so metadata is populated ──────────────────
from app.database.base import Base
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

# ── Your database URL ────────────────────────────────────────────────────
DATABASE_URL = "postgresql+asyncpg://postgres:963010@localhost:5432/ecommerce"


async def create_tables():
    engine = create_async_engine(DATABASE_URL, echo=True)

    print("\n[Database] Creating all tables...\n")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("\n[Database] All tables created successfully!\n")

    # List created tables
    print("[Database] Tables in database:")
    for table_name in Base.metadata.tables.keys():
        print(f"   - {table_name}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
