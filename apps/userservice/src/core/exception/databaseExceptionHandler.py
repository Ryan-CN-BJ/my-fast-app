from fastapi.responses import JSONResponse
from fastapi import Request


def databse_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=422,
        content={
            "code": 400,
            "message": str(exception),
        },
    )
