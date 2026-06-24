from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_by_id_with_relations(self, product_id: int) -> Optional[Product]:
        result = await self.db.execute(
            select(Product)
            .options(
                selectinload(Product.images),
                selectinload(Product.variants),
                selectinload(Product.category),
                selectinload(Product.brand),
            )
            .where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Product]:
        result = await self.db.execute(select(Product).where(Product.slug == slug))
        return result.scalar_one_or_none()

    async def list_products(
        self,
        category_id: int = None,
        brand_id: int = None,
        min_price: float = None,
        max_price: float = None,
        is_featured: bool = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[Product]:
        filters = [Product.is_active == True]
        if category_id:
            filters.append(Product.category_id == category_id)
        if brand_id:
            filters.append(Product.brand_id == brand_id)
        if min_price is not None:
            filters.append(Product.price >= min_price)
        if max_price is not None:
            filters.append(Product.price <= max_price)
        if is_featured is not None:
            filters.append(Product.is_featured == is_featured)

        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Product)
            .options(selectinload(Product.images))
            .where(and_(*filters))
            .offset(offset)
            .limit(page_size)
        )
        return result.scalars().all()
