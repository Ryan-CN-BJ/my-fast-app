from core.middleware import cors
from fastapi import FastAPI
import inspect

MIDDLEWARES = [
    cors.MIDDLEWARE
]


def register_middlewates(app:FastAPI):
    for callabel_obj,args in MIDDLEWARES:
        if inspect.isclass(callabel_obj):
            app.add_middleware(callabel_obj, **args)