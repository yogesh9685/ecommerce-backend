import secrets
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.otp import OTP, OTPPurpose
from app.models.user import User
from app.services.email_service import EmailService
from app.config import settings
from fastapi import HTTPException, status


class OTPService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.email_service = EmailService()

    def _generate_code(self, length: int = 6) -> str:
        return str(secrets.randbelow(10**length)).zfill(length)

    async def send_verification_otp(self, user: User) -> None:
        code = self._generate_code()
        otp = OTP(
            user_id=user.id,
            code=code,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            expires_at=datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
        )
        self.db.add(otp)
        self.email_service.send_otp_email(user.email, code, OTPPurpose.EMAIL_VERIFICATION)

    async def send_password_reset_otp(self, user: User) -> None:
        code = self._generate_code()
        otp = OTP(
            user_id=user.id,
            code=code,
            purpose=OTPPurpose.PASSWORD_RESET,
            expires_at=datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
        )
        self.db.add(otp)
        self.email_service.send_otp_email(user.email, code, OTPPurpose.PASSWORD_RESET)

    async def verify_otp(self, user_id: int, code: str, purpose: OTPPurpose) -> OTP:
        result = await self.db.execute(
            select(OTP).where(
                OTP.user_id == user_id,
                OTP.code == code,
                OTP.purpose == purpose,
                OTP.is_used == False,
            ).order_by(OTP.created_at.desc())
        )
        otp = result.scalar_one_or_none()
        if not otp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
        if otp.is_expired():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP has expired")
        otp.is_used = True
        return otp
