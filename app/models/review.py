from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean, Text
from sqlalchemy.orm import relationship
from app.database.base import Base


class Review(Base):
    __tablename__ = "reviews"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Float, nullable=False)  # 1.0 - 5.0
    title = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)
    is_verified_purchase = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    helpful_count = Column(Integer, default=0)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
