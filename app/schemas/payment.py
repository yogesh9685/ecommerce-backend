from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.payment import PaymentStatus


class PaymentInitiate(BaseModel):
    order_id: int


class PaymentVerify(BaseModel):
    order_id: int
    gateway_payment_id: str
    gateway_order_id: str
    gateway_signature: str


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    gateway: str
    gateway_order_id: Optional[str]
    gateway_payment_id: Optional[str]
    amount: float
    currency: str
    status: PaymentStatus
    created_at: datetime

    class Config:
        from_attributes = True
