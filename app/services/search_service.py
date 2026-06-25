from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.product import Product
from app.models.category import Category
from app.models.brand import Brand


class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, query: str, page: int = 1, page_size: int = 20) -> dict:
        offset = (page - 1) * page_size
        stmt = (
            select(Product)
            .where(
                Product.is_active == True,
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                    Product.sku.ilike(f"%{query}%"),
                ),
            )
            .offset(offset)
            .limit(page_size)
        )
        result = await self.db.execute(stmt)
        products = result.scalars().all()
        return {"results": products, "query": query, "page": page}
