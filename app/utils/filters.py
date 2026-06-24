from typing import Optional
from fastapi import Query


class ProductFilters:
    def __init__(
        self,
        category_id: Optional[int] = Query(None),
        brand_id: Optional[int] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None),
        is_featured: Optional[bool] = Query(None),
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
    ):
        self.category_id = category_id
        self.brand_id = brand_id
        self.min_price = min_price
        self.max_price = max_price
        self.is_featured = is_featured
        self.page = page
        self.page_size = page_size


class OrderFilters:
    def __init__(
        self,
        status: Optional[str] = Query(None),
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
    ):
        self.status = status
        self.page = page
        self.page_size = page_size
