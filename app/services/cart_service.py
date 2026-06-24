from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.cart import CartItem
from app.models.product import Product


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cart(self, user_id: int) -> list[CartItem]:
        result = await self.db.execute(
            select(CartItem).where(CartItem.user_id == user_id)
        )
        return result.scalars().all()

    async def add_to_cart(self, user_id: int, product_id: int, variant_id: int | None, quantity: int) -> CartItem:
        product = await self.db.get(Product, product_id)
        if not product or not product.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        result = await self.db.execute(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
                CartItem.variant_id == variant_id,
            )
        )
        item = result.scalar_one_or_none()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(
                user_id=user_id,
                product_id=product_id,
                variant_id=variant_id,
                quantity=quantity,
                unit_price=product.price,
            )
            self.db.add(item)
        return item

    async def update_cart_item(self, user_id: int, item_id: int, quantity: int) -> CartItem:
        result = await self.db.execute(
            select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        if quantity <= 0:
            await self.db.delete(item)
            return None
        item.quantity = quantity
        return item

    async def remove_from_cart(self, user_id: int, item_id: int) -> None:
        result = await self.db.execute(
            select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        await self.db.delete(item)

    async def clear_cart(self, user_id: int) -> None:
        result = await self.db.execute(select(CartItem).where(CartItem.user_id == user_id))
        for item in result.scalars().all():
            await self.db.delete(item)
