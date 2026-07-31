from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request


def request_validate_exception_handler(
    request: Request, exception: RequestValidationError
):
    error_messages = ", ".join(
        [error.get("msg", "参数校验失败") for error in exception.errors()]
    )

    return JSONResponse(
        status_code=422,
        content={
            "code": 4000,
            "message": f"参数校验失败: {error_messages}",
            # "errors": errors,  # 保留完整的错误列表，方便前端逐个字段展示
        },
    )
