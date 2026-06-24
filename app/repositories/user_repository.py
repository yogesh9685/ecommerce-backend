from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.phone == phone)
        )
        return result.scalar_one_or_none()

    async def list_users(self, page: int = 1, page_size: int = 20) -> list[User]:
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(User).offset(offset).limit(page_size)
        )
        return result.scalars().all()

    async def count(self) -> int:
        from sqlalchemy import func
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar_one()
