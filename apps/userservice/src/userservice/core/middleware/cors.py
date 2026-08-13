from fastapi.middleware.cors import CORSMiddleware
from userservice.core.config.webconfig import webSetting

origins = [o.strip() for o in webSetting.cors_origins.split(",") if o.strip()]

expose_headers = [
    o.strip() for o in webSetting.cors_expose_headers.split(",") if o.strip()
]

print(origins, "origins")
MIDDLEWARE = (
    CORSMiddleware,
    {
        "allow_origins": origins,
        "allow_credentials": False,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "expose_headers": expose_headers,
    },
)


# MIDDLEWARE = (
#     CORSMiddleware,
#     {
#         "allow_origins": origins,
#         "allow_credentials": True,
#         "allow_methods": ["*"],
#         "allow_headers": ["*"],
#         "expose_headers": expose_headers,
#     },
# )
