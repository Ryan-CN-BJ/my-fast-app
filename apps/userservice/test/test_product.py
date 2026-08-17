from httpx import AsyncClient


class TestProduct:
    async def test_create_product(self, async_client: AsyncClient):
        res = await async_client.post(
            "/product/add", json={"brand": "123", "name": "123", "description": "123"}
        )
        print(res, "res")
        data = res.json()["data"]
        assert res.status_code == 200
        assert data["brand"] == "123"
        assert data["id"] is not None
