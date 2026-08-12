from service.base import BaseService
from schema.sku import CreateSku, ResponseSku
from model.sku import Sku
from core.exception.databse import DatabaseException
from model.product import Product


class SkuService(BaseService):
    async def add_sku(self, sku: CreateSku) -> ResponseSku:
        try:
            product = await self.db.get(Product, sku.product_id)
            if product is None:
                raise DatabaseException(
                    original_exception=None, message="所属商品不存在！"
                )
            skuModel = Sku(**sku.model_dump())
            self.db.add(skuModel)
            await self.db.flush()
            return ResponseSku.model_validate(skuModel)
        except Exception as e:
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！"
                )
