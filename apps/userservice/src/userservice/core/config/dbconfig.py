from apps.userservice.src.userservice.core.config.commonConfig import CommonSettings


class DbSetting(CommonSettings):
    user: str = ""
    password: str = ""
    host: str = ""
    port: str = ""
    name: str = ""
    model_config = {"env_prefix": "DB_"}


dbSetting = DbSetting()
