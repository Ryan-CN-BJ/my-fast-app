from core.exception.requestValidateErrorHandler import (
    request_validate_exception_handler,
)

from core.exception.errorHandler import exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI


def register_exception_handler(app: FastAPI):
    app.add_exception_handler(
        RequestValidationError, request_validate_exception_handler
    )
    app.add_exception_handler(Exception, exception_handler)
