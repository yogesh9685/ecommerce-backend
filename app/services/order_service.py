import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import CartItem
from app.models.coupon import Coupon
from app.models.inventory import Inventory
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = OrderRepository(db)

    async def create_order(self, user_id: int, data: OrderCreate) -> Order:
        # Fetch cart items
        cart_result = await self.db.execute(
            select(CartItem).where(CartItem.user_id == user_id)
        )
        cart_items = cart_result.scalars().all()
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
            )

        subtotal = sum(item.unit_price * item.quantity for item in cart_items)
        discount_amount = 0.0

        # Apply coupon
        coupon = None
        if data.coupon_code:
            coupon_result = await self.db.execute(
                select(Coupon).where(
                    Coupon.code == data.coupon_code, Coupon.is_active == True
                )
            )
            coupon = coupon_result.scalar_one_or_none()
            if coupon:
                if coupon.coupon_type.value == "percentage":
                    discount_amount = subtotal * (coupon.discount_value / 100)
                else:
                    discount_amount = coupon.discount_value
                if coupon.max_discount_amount:
                    discount_amount = min(discount_amount, coupon.max_discount_amount)
                coupon.usage_count += 1

        tax_amount = (subtotal - discount_amount) * 0.18  # 18% GST
        shipping_amount = 0.0 if subtotal > 500 else 50.0
        total_amount = subtotal - discount_amount + tax_amount + shipping_amount

        order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
            user_id=user_id,
            shipping_address_id=data.shipping_address_id,
            coupon_id=coupon.id if coupon else None,
            subtotal=subtotal,
            discount_amount=discount_amount,
            tax_amount=tax_amount,
            shipping_amount=shipping_amount,
            total_amount=total_amount,
            notes=data.notes,
        )
        self.db.add(order)
        await self.db.flush()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                variant_id=item.variant_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.unit_price * item.quantity,
            )
            self.db.add(order_item)
            await self.db.delete(item)

        return order

    async def get_order(self, order_id: int, user_id: int) -> Order:
        order = await self.repo.get_by_id(order_id)
        if not order or order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )
        return order

    async def get_user_orders(self, user_id: int, page: int = 1, page_size: int = 20):
        return await self.repo.get_user_orders(user_id, page, page_size)

    async def cancel_order(self, order_id: int, user_id: int) -> Order:
        order = await self.get_order(order_id, user_id)
        if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order cannot be cancelled",
            )
        order.status = OrderStatus.CANCELLED
        return order
