from fastapi.responses import JSONResponse
from fastapi import Request

from fastapi.exceptions import HTTPException


def http_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=422,
        content={
            "code": 4000,
            "message": "123",
        },
    )
