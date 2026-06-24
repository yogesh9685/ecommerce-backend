from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = SearchService(db)
    return await service.search(q, page=page, page_size=page_size)
