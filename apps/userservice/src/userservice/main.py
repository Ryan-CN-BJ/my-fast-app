from fastapi import FastAPI

from apps.userservice.src.userservice.api.user import router as userRouter
from apps.userservice.src.userservice.api.product import router as productRouter
from apps.userservice.src.userservice.api.sku import router as skuRouter
from apps.userservice.src.userservice.api.category import router as categoryRouter

from apps.userservice.src.userservice.core.middleware import register_middlewates
from apps.userservice.src.userservice.core.exception import register_exception_handler
from apps.userservice.src.userservice.schema.response import ErrorResponse

app = FastAPI(responses={"default": {"model": ErrorResponse}})

register_middlewates(app)
register_exception_handler(app)

app.include_router(userRouter)
app.include_router(productRouter)
app.include_router(skuRouter)
app.include_router(categoryRouter)
