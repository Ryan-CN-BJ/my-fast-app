from fastapi import Request
import uuid

from userservice.core.logger.log_record import request_id_var
from userservice.core.logger.request_log import RequestLog


async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)

    log = RequestLog(
        message="请求完成",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else "-",
    )

    request.state.request_log = log
    response = call_next(request)

    if getattr(request.state, "exception_handled", False):
        log.success()
    return response


MIDDLEWARE = (logging_middleware, {})
