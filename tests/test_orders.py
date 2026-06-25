import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_place_order_unauthenticated(client: AsyncClient):
    response = await client.post("/api/v1/orders/", json={
        "shipping_address_id": 1,
    })
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_orders_unauthenticated(client: AsyncClient):
    response = await client.get("/api/v1/orders/")
    assert response.status_code == 403
