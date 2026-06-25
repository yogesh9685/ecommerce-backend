from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, Float, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    slug = Column(String(300), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    sku = Column(String(100), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    compare_price = Column(Float, nullable=True)
    cost_price = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    tags = Column(JSON, nullable=True)
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(String(500), nullable=True)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    images = relationship(
        "ProductImage", back_populates="product", cascade="all, delete-orphan"
    )
    variants = relationship(
        "ProductVariant", back_populates="product", cascade="all, delete-orphan"
    )
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    reviews = relationship("Review", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    wishlist_items = relationship("WishlistItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
