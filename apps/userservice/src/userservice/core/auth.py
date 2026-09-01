from fastapi.security import HTTPBearer
from fastapi import Depends
from typing import Annotated
from utils.auth import verify_token

bear = HTTPBearer()


def get_current_user(token: Annotated[str, Depends(bear)]):
    pass
