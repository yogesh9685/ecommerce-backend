from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.session import get_db
from app.dependencies import get_current_admin
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderStatusUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
async def dashboard(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    total_users = (await db.execute(select(func.count(User.id)))).scalar()
    total_orders = (await db.execute(select(func.count(Order.id)))).scalar()
    total_products = (await db.execute(select(func.count(Product.id)))).scalar()
    total_revenue = (
        await db.execute(
            select(func.sum(Order.total_amount)).where(
                Order.status == OrderStatus.DELIVERED
            )
        )
    ).scalar() or 0.0
    return {
        "total_users": total_users,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_revenue": total_revenue,
    }


@router.get("/orders")
async def list_all_orders(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    repo = OrderRepository(db)
    return await repo.get_all_orders(page, page_size)


@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        from app.core.exceptions import NotFoundException

        raise NotFoundException("Order not found")
    order.status = data.status
    if data.tracking_number:
        order.tracking_number = data.tracking_number
    return {"message": "Order status updated", "status": data.status}


@router.get("/users")
async def list_all_users(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    offset = (page - 1) * page_size
    result = await db.execute(select(User).offset(offset).limit(page_size))
    return result.scalars().all()
