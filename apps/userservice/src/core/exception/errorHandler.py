from fastapi.responses import JSONResponse
from fastapi import Request


def exception_handler(request: Request, exception: Exception):
    print("exception_handler------------")
    return JSONResponse(
        status_code=422,
        content={
            "code": 4000,
            "message": f"{str(exception)}",
        },
    )
