import asyncio
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.config import settings
from app.models.otp import OTP
from app.models.user import User

async def run_auth_test():
    base_url = "http://localhost:8000/api/v1"
    email = "testuser_api@novacart.com"
    password = "MySecurePassword123"
    
    # 1. Register User
    print("\n1. Registering user...")
    async with httpx.AsyncClient() as client:
        reg_resp = await client.post(
            f"{base_url}/auth/register",
            json={
                "full_name": "API Test User",
                "email": email,
                "password": password
            }
        )
        print(f"Register status: {reg_resp.status_code} | Body: {reg_resp.text}")
        if reg_resp.status_code != 201:
            return
            
    # 2. Get OTP from DB
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    otp_code = None
    
    async with async_session() as session:
        result = await session.execute(
            select(OTP, User.email)
            .join(User, OTP.user_id == User.id)
            .where(User.email == email)
            .order_by(OTP.created_at.desc())
        )
        row = result.first()
        if row:
            otp_code = row[0].code
            print(f"Retrieved OTP code from database: {otp_code}")
            
    await engine.dispose()
    
    if not otp_code:
        print("Failed to find OTP code!")
        return
        
    # 3. Verify Email
    print("\n2. Verifying email...")
    async with httpx.AsyncClient() as client:
        ver_resp = await client.post(
            f"{base_url}/auth/verify-email",
            json={
                "email": email,
                "code": otp_code
            }
        )
        print(f"Verification status: {ver_resp.status_code} | Body: {ver_resp.text}")
        
    # 4. Login
    print("\n3. Logging in...")
    async with httpx.AsyncClient() as client:
        log_resp = await client.post(
            f"{base_url}/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        print(f"Login status: {log_resp.status_code} | Body: {log_resp.text}")

if __name__ == "__main__":
    asyncio.run(run_auth_test())
