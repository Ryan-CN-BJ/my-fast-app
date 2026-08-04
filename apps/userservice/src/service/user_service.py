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
            await self.db.flush()  # 因为下面要用到user.id,所以必须flush一次
            return UserResponse(id=user.id, name=user.name, email=user.email)
        except Exception as e:
            print(e, "e")
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！"
                ) from e

    async def get_user_by_id(self, id: int) -> UserResponse:
        try:
            user = await self.db.get(User, id)
            if user is None:
                raise DatabaseException(message="用户不存在")
            return UserResponse(id=user.id, name=user.name, email=user.email)
        except Exception as e:
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！"
                ) from e

    async def get_all_user(self, page, size, name) -> list[UserResponse]:
        try:
            stm = (
                select(User)
                .offset((page - 1) * size)
                .limit(size)
                .order_by(User.id)
                .where(User.name.ilike(f"%{name}%"))
            )
            result = await self.db.execute(stm)
            return [
                UserResponse.model_validate(user) for user in result.scalars().all()
            ]
        except Exception as e:
            raise DatabaseException(message="数据库操作失败！")

    async def del_user(self, id) -> bool:
        try:
            user = await self.db.get(User, id)
            if user is None or user.is_deleted is True:
                raise DatabaseException(message="用户不存在")
            user.is_deleted = True
            return True
        except Exception as e:
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！"
                ) from e

    async def update_user(self, data: UserRegister) -> UserResponse:
        try:
            user = await self.db.get(User, data.id)
            if user is None:
                raise DatabaseException(message="用户不存在！")
            update_data = data.model_dump(exclude_unset=True)
            update_data.pop("id", None)

            for key, value in update_data.items():
                setattr(user, key, value)
            return UserResponse.model_validate(user)
        except Exception as e:
            print("发生了异常～～～～～～")
            if isinstance(e, DatabaseException):
                raise e
            else:
                raise DatabaseException(
                    original_exception=e, message="数据库操作失败！--"
                ) from e
