from userservice.core.exception.base import BaseException
from fastapi import Request
from fastapi.responses import JSONResponse


class AuthException(BaseException):
    pass


def auth_exception_handler(request: Request, exception: AuthException):
    return JSONResponse(
        status_code=422,
        content={
            "code": 4000,
            "message": str(exception),
        },
    )
