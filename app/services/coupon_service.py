from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import datetime

from app.models.coupon import Coupon


class CouponService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def validate_coupon(self, code: str, order_amount: float) -> Coupon:
        result = await self.db.execute(
            select(Coupon).where(Coupon.code == code, Coupon.is_active == True)
        )
        coupon = result.scalar_one_or_none()
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid coupon code"
            )
        if coupon.expires_at and datetime.utcnow() > coupon.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Coupon has expired"
            )
        if coupon.usage_limit and coupon.usage_count >= coupon.usage_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon usage limit reached",
            )
        if order_amount < coupon.min_order_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Minimum order amount ₹{coupon.min_order_amount} required",
            )
        return coupon

    async def create_coupon(self, data: dict) -> Coupon:
        coupon = Coupon(**data)
        self.db.add(coupon)
        return coupon

    async def list_coupons(self) -> list[Coupon]:
        result = await self.db.execute(select(Coupon))
        return result.scalars().all()
