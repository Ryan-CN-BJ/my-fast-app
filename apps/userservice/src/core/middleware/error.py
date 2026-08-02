import json

from fastapi import Request
from fastapi.responses import JSONResponse


async def global_exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        return JSONResponse(
            status_code=422,
            content={
                "code": 400,
                "message": str(exc),
            },
        )


MIDDLEWARE = (global_exception_middleware, {})
