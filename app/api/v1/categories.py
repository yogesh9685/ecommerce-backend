from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.dependencies import get_current_admin
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.utils.helpers import slugify

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.is_active == True))
    return result.scalars().all()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        from app.core.exceptions import NotFoundException

        raise NotFoundException("Category not found")
    return category


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    category = Category(**data.model_dump(), slug=slugify(data.name))
    db.add(category)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        from app.core.exceptions import NotFoundException

        raise NotFoundException("Category not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(category, field, value)
    return category


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if category:
        await db.delete(category)
