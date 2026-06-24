from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    url = Column(String(512), nullable=False)
    alt_text = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    product = relationship("Product", back_populates="images")
