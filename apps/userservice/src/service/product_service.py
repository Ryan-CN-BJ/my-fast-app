from service.base import BaseService

from schema.product import CreateProduct, ResponseProduct
from model.product import Product
from core.exception.databse import DatabaseException


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
