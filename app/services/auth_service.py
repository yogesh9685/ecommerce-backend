from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import timedelta

from app.models.user import User
from app.models.session import Session
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_refresh_token
)
from app.repositories.user_repository import UserRepository
from app.services.otp_service import OTPService
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.config import settings
from datetime import datetime


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.otp_service = OTPService(db)

    async def register(self, data: RegisterRequest) -> User:
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        user = User(
            email=data.email,
            full_name=data.full_name,
            phone=data.phone,
            hashed_password=hash_password(data.password),
            is_verified=True,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(data.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email")

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        session = Session(
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        self.db.add(session)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        payload = decode_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        result = await self.db.execute(
            select(Session).where(Session.refresh_token == refresh_token, Session.is_active == True)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

        session.is_active = False
        new_access = create_access_token({"sub": payload["sub"]})
        new_refresh = create_refresh_token({"sub": payload["sub"]})
        new_session = Session(
            user_id=session.user_id,
            refresh_token=new_refresh,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        self.db.add(new_session)
        return TokenResponse(access_token=new_access, refresh_token=new_refresh)

    async def logout(self, refresh_token: str) -> None:
        result = await self.db.execute(
            select(Session).where(Session.refresh_token == refresh_token)
        )
        session = result.scalar_one_or_none()
        if session:
            session.is_active = False
