from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    items = await service.get_cart(current_user.id)
    subtotal = sum(i.unit_price * i.quantity for i in items)
    return CartResponse(
        items=[
            {
                "id": i.id,
                "product_id": i.product_id,
                "variant_id": i.variant_id,
                "quantity": i.quantity,
                "unit_price": i.unit_price,
                "total_price": i.unit_price * i.quantity,
            }
            for i in items
        ],
        subtotal=subtotal,
        item_count=len(items),
    )


@router.post("/items", status_code=201)
async def add_to_cart(
    data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    item = await service.add_to_cart(
        current_user.id, data.product_id, data.variant_id, data.quantity
    )
    return {"message": "Item added to cart", "item_id": item.id}


@router.put("/items/{item_id}")
async def update_cart_item(
    item_id: int,
    data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    await service.update_cart_item(current_user.id, item_id, data.quantity)
    return {"message": "Cart updated"}


@router.delete("/items/{item_id}", status_code=204)
async def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    await service.remove_from_cart(current_user.id, item_id)


@router.delete("/", status_code=204)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    await service.clear_cart(current_user.id)
