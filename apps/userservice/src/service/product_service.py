from service.base import BaseService

from schema.product import (
    CreateProduct,
    ResponseProduct,
    ResponseProductWithSkus,
    ResponseProductWithCates,
)
from model.product import Product
from model.category import Category
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

    async def add_cate_to_product(
        self, product_id: int, cate_ids: list[int]
    ) -> ResponseProductWithCates:
        try:
            stm = (
                select(Product)
                .options(selectinload(Product.cates))
                .where(Product.id == product_id)
            )
            productModel = (await self.db.execute(stm)).scalar()
            if productModel is None:
                raise DatabaseException(message="商品不存在！")

            if len(cate_ids) != len(set(cate_ids)):
                raise DatabaseException(message="商品种类重复！")

            cates: list[Category] = (
                (
                    await self.db.execute(
                        select(Category).where(Category.id.in_(cate_ids))
                    )
                )
                .scalars()
                .all()
            )

            found_ids = {c.id for c in cates}
            missing_ids = set(cate_ids) - found_ids
            if missing_ids:
                raise DatabaseException(
                    message=f"以下分类不存在，{sorted(missing_ids)}"
                )

            produceCates = productModel.cates
            existing_ids = {c.id for c in produceCates}
            duplicated_ids = existing_ids & set(cate_ids)
            if duplicated_ids:
                raise DatabaseException(
                    message=f"以下分类已经关联，请勿重复添加：{sorted(duplicated_ids)}"
                )
            productModel.cates.extend(cates)
            return ResponseProductWithCates.model_validate(productModel)
        except Exception as e:
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！"
                )

    async def update_product_cates(
        self, product_id: int, cate_ids: list[int]
    ) -> ResponseProductWithCates:
        if len(cate_ids) != len(set(cate_ids)):
            raise DatabaseException(message="商品种类重复！")
        stm = (
            select(Product)
            .options(selectinload(Product.cates))
            .where(Product.id == product_id)
        )
        productModel = (await self.db.execute(stm)).scalar()

        if productModel is None:
            raise DatabaseException(message="商品不存在！")

        cates = (
            (await self.db.execute(select(Category).where(Category.id.in_(cate_ids))))
            .scalars()
            .all()
        )
        if len(cates) != len(cate_ids):
            missing = set(cate_ids) - {c.id for c in cates}
            raise DatabaseException(message=f"以下商品种类不合法,{sorted(missing)}")

        productModel.cates = cates
        await self.db.flush()
        return ResponseProductWithCates.model_validate(productModel)
