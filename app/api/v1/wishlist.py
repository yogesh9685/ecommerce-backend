from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.wishlist import WishlistItem

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("/")
async def get_wishlist(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(WishlistItem).where(WishlistItem.user_id == current_user.id))
    return result.scalars().all()


@router.post("/{product_id}", status_code=201)
async def add_to_wishlist(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WishlistItem).where(
            WishlistItem.user_id == current_user.id,
            WishlistItem.product_id == product_id,
        )
    )
    if result.scalar_one_or_none():
        return {"message": "Already in wishlist"}
    item = WishlistItem(user_id=current_user.id, product_id=product_id)
    db.add(item)
    return {"message": "Added to wishlist"}


@router.delete("/{product_id}", status_code=204)
async def remove_from_wishlist(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(WishlistItem).where(
            WishlistItem.user_id == current_user.id,
            WishlistItem.product_id == product_id,
        )
    )
    item = result.scalar_one_or_none()
    if item:
        await db.delete(item)
