from fastapi import FastAPI

from userservice.api.user import router as userRouter
from userservice.api.product import router as productRouter
from userservice.api.sku import router as skuRouter
from userservice.api.category import router as categoryRouter

from userservice.core.middleware import register_middlewates
from userservice.core.exception import register_exception_handler
from userservice.schema.response import ErrorResponse
from userservice.core.db import get_session_factory
from userservice.service.setting_service import SettingService
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_session_factory().begin() as session:
        await SettingService(db=session).initialize()
    yield


app = FastAPI(lifespan=lifespan, responses={"default": {"model": ErrorResponse}})

register_middlewates(app)
register_exception_handler(app)

app.include_router(userRouter)
app.include_router(productRouter)
app.include_router(skuRouter)
app.include_router(categoryRouter)
