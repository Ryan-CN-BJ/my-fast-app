import json

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError


async def global_exception_middleware(request: Request, call_next):
    response = await call_next(request)
    return response


MIDDLEWARE = (global_exception_middleware, {})
