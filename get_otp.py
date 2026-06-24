import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.config import settings
from app.models.otp import OTP
from app.models.user import User

async def get_latest_otp():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        result = await session.execute(
            select(OTP, User.email)
            .join(User, OTP.user_id == User.id)
            .order_by(OTP.created_at.desc())
            .limit(5)
        )
        rows = result.all()
        if not rows:
            print("No OTP records found in the database.")
            return
        print("\n--- Latest 5 OTP Codes ---")
        for otp, email in rows:
            print(f"Email: {email} | OTP Code: {otp.code} | Purpose: {otp.purpose} | Used: {otp.is_used}")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(get_latest_otp())
