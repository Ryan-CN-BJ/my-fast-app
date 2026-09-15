from userservice.core.config.commonConfig import CommonSettings


class LogSetting(CommonSettings):
    level: str
    slow_query_threshold: str
    model_config = {"env_prefix": "LOG_"}


logSetting = LogSetting()
