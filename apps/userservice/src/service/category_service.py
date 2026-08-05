from service.base import BaseService
from schema.category import CreateCategory, ResponseCategory
from model.category import Category
from core.exception.databse import DatabaseException


class CategoruService(BaseService):
    async def add_category(self, createCategory: CreateCategory) -> ResponseCategory:
        try:
            modelCategory = Category(**createCategory.model_dump())
            self.db.add(modelCategory)
            await self.db.flush()
            return ResponseCategory.model_validate(modelCategory)
        except Exception as e:
            raise DatabaseException(original_exception=e, message="数据库操作失败！")
