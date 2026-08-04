from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request


def request_validate_exception_handler(request: Request, exception: Exception):
    assert isinstance(exception, RequestValidationError)
    # error_messages = ", ".join(
    #     [error.get("msg", "参数校验失败") for error in exception.errors()]
    # )
    errors = []
    for error in exception.errors():
        print(error["loc"], 'error["loc"]')
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append(
            {
                "field": field,
                "message": error["msg"],
                "type": error["type"],
                "input_value": error.get("input"),
            }
        )

    return JSONResponse(
        status_code=422,
        content={"code": 400, "message": f"参数校验失败", "errors": errors},
    )
