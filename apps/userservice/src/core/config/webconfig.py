from core.config.commonConfig import CommonSettings

class WebSetting(CommonSettings):
    cors_origins: str = ""  # 实际读取 WEB_CORS_ORIGINS，多个来源用逗号分隔
    cors_expose_headers: str = ""  # 实际读取 WEB_CORS_EXPOSE_HEADERS
    model_config = {"env_prefix": "WEB_"}

webSetting = WebSetting()