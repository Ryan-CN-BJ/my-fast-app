from httpx import AsyncClient
import pytest


class TestProduct:
    async def test_create_product(self, async_client: AsyncClient):
        res = await async_client.post(
            "/product/add",
            json={"brand": "123", "name": "测试pytest", "description": "123"},
        )
        print(res, "res")
        data = res.json()["data"]
        assert res.status_code == 200
        assert data["brand"] == "123"
        assert data["id"] is not None

    @pytest.mark.smoke
    async def test_create_get_product(self, async_client: AsyncClient):
        res = await async_client.post(
            "/product/add",
            json={"brand": "mrj", "name": "测试pytest", "description": "123"},
        )
        id = res.json()["data"]["id"]

        response = await async_client.get(
            "/product/query/productwithskus", params={"id": id}
        )
        product = response.json()["data"]
        assert product["brand"] == "mrj"
        assert product["name"] == "测试pytest"
