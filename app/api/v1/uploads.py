from fastapi import APIRouter, Depends, UploadFile, File

from app.dependencies import get_current_user
from app.models.user import User
from app.services.upload_service import UploadService

router = APIRouter(prefix="/uploads", tags=["Uploads"])


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    folder: str = "general",
    current_user: User = Depends(get_current_user),
):
    service = UploadService()
    url = await service.upload_image(file, folder=folder)
    return {"url": url}


@router.post("/product-image")
async def upload_product_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    service = UploadService()
    url = await service.upload_image(file, folder="products")
    return {"url": url}


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    service = UploadService()
    url = await service.upload_image(file, folder="avatars")
    return {"url": url}
