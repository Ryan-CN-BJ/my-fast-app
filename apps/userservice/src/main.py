from fastapi import FastAPI

from api.user import router as userRouter

from core.middleware import register_middlewates
from core.exception import register_exception_handler

app = FastAPI()

register_middlewates(app)
register_exception_handler(app)

app.include_router(userRouter)

