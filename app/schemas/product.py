from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductImageResponse(BaseModel):
    id: int
    url: str
    alt_text: Optional[str]
    is_primary: bool

    class Config:
        from_attributes = True


class ProductVariantResponse(BaseModel):
    id: int
    name: str
    value: str
    sku: str
    price: Optional[float]
    stock: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    sku: str
    price: float = Field(..., gt=0)
    compare_price: Optional[float] = None
    category_id: int
    brand_id: Optional[int] = None
    is_active: bool = True
    is_featured: bool = False
    tags: Optional[List[str]] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    compare_price: Optional[float] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    tags: Optional[List[str]] = None


class ProductResponse(ProductBase):
    id: int
    slug: str
    average_rating: float
    total_reviews: int
    # images:  List[ProductImageResponse] = []
    # variants: List[ProductVariantResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    id: int
    name: str
    slug: str
    price: float
    compare_price: Optional[float]
    average_rating: float
    total_reviews: int
    images: List[ProductImageResponse] = []

    class Config:
        from_attributes = True
