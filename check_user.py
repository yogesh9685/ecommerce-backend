import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.config import settings
from app.models.user import User
from app.core.security import verify_password

async def test_user_password():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    email_to_check = "yogeshgiri182@gmail.com" # adjust to the user's input
    password_to_check = "userpassword" # standard dummy password
    
    async with async_session() as session:
        # Check standard users
        result = await session.execute(
            select(User)
        )
        users = result.scalars().all()
        print("\n--- Registered Users ---")
        for u in users:
            match_p1 = verify_password("userpassword", u.hashed_password)
            match_p2 = verify_password("adminpassword", u.hashed_password)
            print(f"ID: {u.id} | Email: {u.email} | Superuser: {u.is_superuser} | Verified: {u.is_verified} | Hashed PW: {u.hashed_password}")
            print(f"  -> Match 'userpassword'?: {match_p1} | Match 'adminpassword'?: {match_p2}")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_user_password())
