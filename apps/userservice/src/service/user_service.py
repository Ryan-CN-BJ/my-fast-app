from service.base import BaseService
from schema.user import UserRegister, UserResponse

from model.user import User
from sqlalchemy import select

from core.exception.databse import DatabaseException


class UserService(BaseService):
    async def regiser_user(self, data: UserRegister) -> UserResponse:
        # 查询
        stm = select(User).where(User.email == data.email)
        existing_user = await self.db.scalar(stm)

        if existing_user:
            raise ValueError("该用户已存在！")

        user = User(**data.model_dump(exclude={"confirmPwd"}))
        try:
            self.db.add(user)
            await self.db.flush()
        except Exception as e:
            raise DatabaseException(
                original_exception=e, message="数据库操作失败！"
            ) from e

        return UserResponse(id=user.id, name=user.name)
