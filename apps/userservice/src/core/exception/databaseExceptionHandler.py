from fastapi.responses import JSONResponse
from fastapi import Request
from core.exception.databse import DatabaseException


def databse_exception_handler(request: Request, exception: Exception):
    assert isinstance(exception, DatabaseException)
    print(exception.original_exception, "exception")
    return JSONResponse(
        status_code=422,
        content={
            "code": 400,
            "message": str(exception),
        },
    )
