from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)
from app.services.product_service import ProductService
from app.utils.filters import ProductFilters

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductListResponse])
async def list_products(
    filters: ProductFilters = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    return await service.list_products(
        category_id=filters.category_id,
        brand_id=filters.brand_id,
        min_price=filters.min_price,
        max_price=filters.max_price,
        is_featured=filters.is_featured,
        page=filters.page,
        page_size=filters.page_size,
    )


@router.get("/{slug}")
async def get_product(slug: str, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)

    return await service.get_product_by_slug(slug)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(db)
    return await service.create_product(data)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(db)
    return await service.update_product(product_id, data)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(db)
    await service.delete_product(product_id)
