from apps.userservice.src.userservice.core.exception.requestValidateErrorHandler import (
    request_validate_exception_handler,
)

from apps.userservice.src.userservice.core.exception.errorHandler import (
    exception_handler,
)
from apps.userservice.src.userservice.core.exception.httpExceptionHandler import (
    http_exception_handler,
)
from apps.userservice.src.userservice.core.exception.databaseExceptionHandler import (
    databse_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI

from starlette.exceptions import HTTPException
from apps.userservice.src.userservice.core.exception.databse import DatabaseException


def register_exception_handler(app: FastAPI):
    app.add_exception_handler(DatabaseException, databse_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(
        RequestValidationError, request_validate_exception_handler
    )
    # app.add_exception_handler(Exception, exception_handler)
