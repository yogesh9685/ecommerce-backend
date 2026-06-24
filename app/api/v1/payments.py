from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.payment import PaymentInitiate, PaymentVerify, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/initiate")
async def initiate_payment(
    data: PaymentInitiate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = PaymentService(db)
    return await service.initiate_payment(data.order_id, current_user.id)


@router.post("/verify", response_model=PaymentResponse)
async def verify_payment(
    data: PaymentVerify,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = PaymentService(db)
    return await service.verify_payment(
        data.order_id,
        data.gateway_payment_id,
        data.gateway_order_id,
        data.gateway_signature,
    )
