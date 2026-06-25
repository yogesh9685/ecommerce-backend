from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from app.database.session import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    OTPVerifyRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from app.services.auth_service import AuthService
from app.services.otp_service import OTPService
from app.models.otp import OTPPurpose
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.register(data)
    return {
        "message": "Registration successful. Please verify your email.",
        "user_id": user.id,
    }


@limiter.limit("5/minute")
@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request, data: LoginRequest, db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.refresh_tokens(data.refresh_token)


@router.post("/logout")
async def logout(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    await service.logout(data.refresh_token)
    return {"message": "Logged out successfully"}


@router.post("/verify-email")
async def verify_email(data: OTPVerifyRequest, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_email(data.email)
    otp_service = OTPService(db)
    await otp_service.verify_otp(user.id, data.code, OTPPurpose.EMAIL_VERIFICATION)
    user.is_verified = True
    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
async def forgot_password(
    data: PasswordResetRequest, db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get_by_email(data.email)
    if user:
        otp_service = OTPService(db)
        await otp_service.send_password_reset_otp(user)
    return {"message": "If the email exists, a reset OTP has been sent"}


@router.post("/reset-password")
async def reset_password(
    data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.get_by_email(data.email)
    otp_service = OTPService(db)
    await otp_service.verify_otp(user.id, data.code, OTPPurpose.PASSWORD_RESET)
    user.hashed_password = hash_password(data.new_password)
    return {"message": "Password reset successful"}


@router.post("/resend-otp")
async def resend_otp(data: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_email(data.email)
    if not user:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        return {"message": "Email already verified"}
    otp_service = OTPService(db)
    await otp_service.send_verification_otp(user)
    return {"message": "Verification OTP resent successfully"}
