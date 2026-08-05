from service.base import BaseService

from schema.product import CreateProduct, ResponseProduct, ResponseProductWithSkus
from model.product import Product
from core.exception.databse import DatabaseException
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class ProductService(BaseService):
    async def add_product(self, product: CreateProduct) -> ResponseProduct:
        try:
            productModel = Product(**product.model_dump())
            self.db.add(productModel)
            await self.db.flush()
            res = ResponseProduct.model_validate(productModel)
            return res
        except Exception as e:
            raise DatabaseException(message="数据库操作失败！", original_exception=e)

    async def get_product_width_sku(self, id: int) -> ResponseProductWithSkus:
        stm = (
            select(Product).options(selectinload(Product.skus)).where(Product.id == id)
        )
        productModel = await self.db.scalar(stm)
        return ResponseProductWithSkus.model_validate(productModel)
