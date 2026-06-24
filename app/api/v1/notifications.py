from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/")
async def get_notifications(current_user: User = Depends(get_current_user)):
    # TODO: fetch from DB or Redis stream
    return {"notifications": [], "unread_count": 0}


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
):
    return {"message": "Notification marked as read"}


@router.post("/read-all")
async def mark_all_read(current_user: User = Depends(get_current_user)):
    return {"message": "All notifications marked as read"}
