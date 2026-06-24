from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from app.database.base import Base


class Session(Base):
    __tablename__ = "sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    refresh_token = Column(String(512), unique=True, nullable=False)
    device_info = Column(String(255), nullable=True)
    ip_address = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=False)
