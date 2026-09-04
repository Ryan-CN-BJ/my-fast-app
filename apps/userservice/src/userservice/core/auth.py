from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from typing import Annotated
from utils.auth import verify_token
from userservice.core.config.webconfig import webSetting
from userservice.core.exception.auth import AuthException
from userservice.core.db import get_db
from userservice.model.user import User
from userservice.schema.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy import select

bear = HTTPBearer()


async def get_current_user(
    cred: Annotated[HTTPAuthorizationCredentials, Depends(bear)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    try:
        data = verify_token(
            token=cred.credentials, secret_key=webSetting.jwt_secret_key
        )
        userId = data.get("userId")
        if userId is None:
            raise AuthException(message="认证失败！")
        stm = select(User).where(User.id == userId)
        res = await db.execute(stm)
        dbUser = res.scalar_one()
        return UserResponse.model_validate(dbUser)
    except:
        raise AuthException(message="认证失败！")
