from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.brand import BrandCreate
from app.database.session import get_db
from app.dependencies import get_current_admin
from app.models.brand import Brand
from app.utils.helpers import slugify

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/")
async def list_brands(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand).where(Brand.is_active == True))
    return result.scalars().all()


@router.get("/{brand_id}")
async def get_brand(brand_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    if not brand:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("Brand not found")
    return brand

@router.post("/", status_code=201)
async def create_brand(
    data: BrandCreate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    brand = Brand(
        **data.model_dump(),
        slug=slugify(data.name),
    )

    db.add(brand)

    await db.commit()
    await db.refresh(brand)

    return brand


@router.delete("/{brand_id}", status_code=204)
async def delete_brand(
    brand_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    if brand:
        await db.delete(brand)
