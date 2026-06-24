from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        result = await self.db.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_by_gateway_payment_id(self, gateway_payment_id: str) -> Optional[Payment]:
        result = await self.db.execute(
            select(Payment).where(Payment.gateway_payment_id == gateway_payment_id)
        )
        return result.scalar_one_or_none()
