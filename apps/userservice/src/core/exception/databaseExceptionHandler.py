from fastapi.responses import JSONResponse
from fastapi import Request
from core.exception.databse import DatabaseException
from sqlalchemy.exc import IntegrityError


def databse_exception_handler(request: Request, exception: Exception):
    assert isinstance(exception, DatabaseException)
    print(
        "__class__",
        exception.original_exception.__class__,
        exception.original_exception,
        "exception",
    )
    if exception.original_exception and isinstance(
        exception.original_exception, IntegrityError
    ):
        e = exception.original_exception
        detail = str(e.orig)
        return JSONResponse(
            status_code=422,
            content={
                "code": 400,
                "message": detail.split(":  ")[-1],
            },
        )
    else:
        return JSONResponse(
            status_code=422,
            content={
                "code": 400,
                "message": str(exception),
            },
        )
