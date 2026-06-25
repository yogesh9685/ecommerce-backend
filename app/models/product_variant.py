from sqlalchemy import Column, String, Integer, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base


class ProductVariant(Base):
    __tablename__ = "product_variants"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g. "Color", "Size"
    value = Column(String(100), nullable=False)  # e.g. "Red", "XL"
    sku = Column(String(100), unique=True, nullable=False)
    price = Column(Float, nullable=True)
    stock = Column(Integer, default=0)
    attributes = Column(JSON, nullable=True)

    product = relationship("Product", back_populates="variants")
