from fastapi.responses import JSONResponse
from fastapi import Request
from userservice.core.exception.databse import DatabaseException
from sqlalchemy.exc import IntegrityError


def databse_exception_handler(request: Request, exception: Exception):
    request.state.exception_handled = True
    assert isinstance(exception, DatabaseException)

    # 日志记录
    request_log = request.state.request_log
    if request_log:
        request_log.message = "请求异常"
        request_log.warning()

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
