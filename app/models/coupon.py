from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum


class CouponType(str, enum.Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    FREE_SHIPPING = "free_shipping"


class Coupon(Base):
    __tablename__ = "coupons"

    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    coupon_type = Column(Enum(CouponType), nullable=False)
    discount_value = Column(Float, nullable=False)
    min_order_amount = Column(Float, default=0.0)
    max_discount_amount = Column(Float, nullable=True)
    usage_limit = Column(Integer, nullable=True)
    usage_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)

    orders = relationship("Order", back_populates="coupon")
