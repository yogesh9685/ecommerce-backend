import asyncio
import httpx


async def test_me():
    base_url = "http://localhost:8000/api/v1"
    email = "user@novacart.com"
    password = "userpassword"

    async with httpx.AsyncClient() as client:
        # 1. Login
        log_resp = await client.post(
            f"{base_url}/auth/login", json={"email": email, "password": password}
        )
        print(f"Login status: {log_resp.status_code}")
        if log_resp.status_code != 200:
            print("Login failed!")
            return

        token = log_resp.json()["access_token"]

        # 2. Call /users/me
        headers = {"Authorization": f"Bearer {token}"}
        me_resp = await client.get(f"{base_url}/users/me", headers=headers)
        print(f"Me status: {me_resp.status_code} | Body: {me_resp.text}")


if __name__ == "__main__":
    asyncio.run(test_me())
