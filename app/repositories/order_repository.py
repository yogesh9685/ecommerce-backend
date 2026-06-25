from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items), selectinload(Order.payment))
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_user_orders(
        self, user_id: int, page: int = 1, page_size: int = 20
    ) -> list[Order]:
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        return result.scalars().all()

    async def get_all_orders(self, page: int = 1, page_size: int = 20) -> list[Order]:
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        return result.scalars().all()
