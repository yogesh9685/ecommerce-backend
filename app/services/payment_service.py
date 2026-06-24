import razorpay
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.payment import Payment, PaymentStatus
from app.models.order import Order, OrderStatus
from app.repositories.payment_repository import PaymentRepository
from app.config import settings
import hmac, hashlib


class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = PaymentRepository(db)
        if settings.PAYMENT_GATEWAY == "razorpay":
            self.client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

    async def initiate_payment(self, order_id: int, user_id: int) -> dict:
        result = await self.db.execute(
            select(Order).where(Order.id == order_id, Order.user_id == user_id)
        )
        order = result.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        gateway_order = self.client.order.create({
            "amount": int(order.total_amount * 100),
            "currency": "INR",
            "receipt": order.order_number,
        })

        payment = Payment(
            order_id=order.id,
            gateway="razorpay",
            gateway_order_id=gateway_order["id"],
            amount=order.total_amount,
            currency="INR",
            status=PaymentStatus.PENDING,
        )
        self.db.add(payment)

        return {
            "gateway_order_id": gateway_order["id"],
            "amount": order.total_amount,
            "currency": "INR",
            "key_id": settings.RAZORPAY_KEY_ID,
        }

    async def verify_payment(
        self, order_id: int, gateway_payment_id: str, gateway_order_id: str, gateway_signature: str
    ) -> Payment:
        result = await self.db.execute(select(Payment).where(Payment.order_id == order_id))
        payment = result.scalar_one_or_none()
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

        # Verify signature
        body = f"{gateway_order_id}|{gateway_payment_id}"
        expected = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(), body.encode(), hashlib.sha256
        ).hexdigest()

        if expected != gateway_signature:
            payment.status = PaymentStatus.FAILED
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment verification failed")

        payment.gateway_payment_id = gateway_payment_id
        payment.gateway_signature = gateway_signature
        payment.status = PaymentStatus.SUCCESS

        order_result = await self.db.execute(select(Order).where(Order.id == order_id))
        order = order_result.scalar_one()
        order.status = OrderStatus.CONFIRMED
        return payment
