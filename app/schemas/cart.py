from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CartItemBase(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    variant_id: Optional[int]
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    items: List[CartItemResponse]
    subtotal: float
    item_count: int
