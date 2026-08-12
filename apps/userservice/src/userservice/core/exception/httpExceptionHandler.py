from fastapi.responses import JSONResponse
from fastapi import Request


from starlette.exceptions import HTTPException


def http_exception_handler(request: Request, exception: Exception):
    print("http_exception_handler-----")
    return JSONResponse(
        status_code=422,
        content={
            "code": 4000,
            "message": str(exception),
        },
    )
