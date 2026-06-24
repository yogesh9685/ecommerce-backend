from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies import get_current_admin
from app.services.coupon_service import CouponService

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.get("/validate")
async def validate_coupon(
    code: str = Query(...),
    order_amount: float = Query(...),
    db: AsyncSession = Depends(get_db),
):
    service = CouponService(db)
    coupon = await service.validate_coupon(code, order_amount)
    return {
        "code": coupon.code,
        "type": coupon.coupon_type,
        "discount_value": coupon.discount_value,
        "max_discount": coupon.max_discount_amount,
    }


@router.get("/")
async def list_coupons(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    service = CouponService(db)
    return await service.list_coupons()


@router.post("/", status_code=201)
async def create_coupon(
    data: dict,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    service = CouponService(db)
    coupon = await service.create_coupon(data)
    return coupon
