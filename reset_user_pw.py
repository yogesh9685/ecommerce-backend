import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.config import settings
from app.models.user import User
from app.core.security import hash_password

async def reset_passwords():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    emails = ["yogeshgiri182@gmail.com", "aaa@gmail.com", "abc@gmail.com", "testuser_api@novacart.com"]
    new_hashed = hash_password("userpassword")
    
    async with async_session() as session:
        for email in emails:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if user:
                user.hashed_password = new_hashed
                user.is_verified = True # ensure verified
                user.is_active = True # ensure active
                print(f"Successfully reset password for {email} to 'userpassword' and set verified=True")
                
        await session.commit()
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(reset_passwords())
