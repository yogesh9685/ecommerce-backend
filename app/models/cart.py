from sqlalchemy import Column, Integer, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=True)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    variant = relationship("ProductVariant")
