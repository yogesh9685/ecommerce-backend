from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Enum, DateTime
from app.database.base import Base
import enum
from datetime import datetime


class OTPPurpose(str, enum.Enum):
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    PHONE_VERIFICATION = "phone_verification"


class OTP(Base):
    __tablename__ = "otps"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    code = Column(String(10), nullable=False)
    purpose = Column(Enum(OTPPurpose), nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at
