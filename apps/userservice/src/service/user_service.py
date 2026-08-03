from service.base import BaseService
from schema.user import UserRegister, UserResponse

from model.user import User
from sqlalchemy import select

from core.exception.databse import DatabaseException


class UserService(BaseService):
    async def regiser_user(self, data: UserRegister) -> UserResponse:
        # 查询
        try:
            stm = select(User).where(User.email == data.email)
            existing_user = await self.db.scalar(stm)

            if existing_user:
                raise DatabaseException("该用户已存在！")
            user = User(**data.model_dump(exclude={"confirmPwd"}))
            self.db.add(user)
            await self.db.flush()
        except Exception as e:
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！"
                ) from e
        return UserResponse(id=user.id, name=user.name, email=user.email)

    async def get_user_by_id(self, id: int) -> UserResponse:
        try:
            user = await self.db.get(User, id)
            if user is None:
                raise DatabaseException(message="用户不存在")
        except Exception as e:
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！"
                ) from e

        return UserResponse(id=user.id, name=user.name, email=user.email)

    async def get_all_user(self, page, size, name) -> list[UserResponse]:
        stm = (
            select(User)
            .offset((page - 1) * size)
            .limit(size)
            .order_by(User.id)
            .where(User.name.ilike(f"%{name}%"))
        )
        result = await self.db.execute(stm)
        return [
            UserResponse(name=user.name, email=user.email, id=user.id)
            for user in result.scalars().all()
        ]

    async def del_user(self, id) -> bool:
        try:
            user = await self.db.get(User, id)
            if user is None:
                raise DatabaseException(message="用户不存在")
            await self.db.delete(user)
        except Exception as e:
            print(e, "e")
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！"
                ) from e
        return True
