from userservice.core.middleware import cors
from userservice.core.middleware import error

from fastapi import FastAPI
import inspect

MIDDLEWARES = [cors.MIDDLEWARE, error.MIDDLEWARE]


def register_middlewates(app: FastAPI):
    for callable_obj, args in MIDDLEWARES:
        if inspect.isclass(callable_obj):
            app.add_middleware(callable_obj, **args)
        else:
            app.middleware("http")(callable_obj, **args)
