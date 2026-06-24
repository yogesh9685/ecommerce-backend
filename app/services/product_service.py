from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.product import Product
from app.models.inventory import Inventory
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.helpers import slugify


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProductRepository(db)

    async def create_product(self, data: ProductCreate) -> Product:
        slug = slugify(data.name)
        existing = await self.repo.get_by_slug(slug)
        if existing:
            slug = f"{slug}-{data.sku.lower()}"
        product = Product(**data.model_dump(), slug=slug)
        self.db.add(product)
        await self.db.flush()
        inventory = Inventory(product_id=product.id, quantity=0)
        self.db.add(inventory)
        return product

    async def get_product(self, product_id: int) -> Product:
        product = await self.repo.get_by_id_with_relations(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    async def get_product_by_slug(self, slug: str) -> Product:
        product = await self.repo.get_by_slug(slug)
      
        return product

    async def list_products(
        self,
        category_id: int = None,
        brand_id: int = None,
        min_price: float = None,
        max_price: float = None,
        is_featured: bool = None,
        page: int = 1,
        page_size: int = 20,
    ):
        return await self.repo.list_products(
            category_id=category_id,
            brand_id=brand_id,
            min_price=min_price,
            max_price=max_price,
            is_featured=is_featured,
            page=page,
            page_size=page_size,
        )

    async def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(product, field, value)
        return product

    async def delete_product(self, product_id: int) -> None:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        await self.db.delete(product)
