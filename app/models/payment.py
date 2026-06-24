from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    gateway = Column(String(50), nullable=False)         # razorpay / stripe
    gateway_order_id = Column(String(200), nullable=True)
    gateway_payment_id = Column(String(200), nullable=True)
    gateway_signature = Column(String(500), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    failure_reason = Column(String(500), nullable=True)
    raw_response = Column(JSON, nullable=True)

    order = relationship("Order", back_populates="payment")
