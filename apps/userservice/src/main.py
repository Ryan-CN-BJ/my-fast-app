from fastapi import FastAPI

from api.user import router as userRouter

from core.middleware import register_middlewates
from core.exception import register_exception_handler
from schema.response import ErrorResponse

app = FastAPI(responses={"default": {"model": ErrorResponse}})

register_middlewates(app)
register_exception_handler(app)

app.include_router(userRouter)
