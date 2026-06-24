import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_products(client: AsyncClient):
    response = await client.get("/api/v1/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    response = await client.get("/api/v1/products/nonexistent-slug")
    assert response.status_code == 404
