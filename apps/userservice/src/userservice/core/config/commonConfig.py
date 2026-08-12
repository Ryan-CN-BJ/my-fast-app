from pydantic_settings import BaseSettings

class CommonSettings(BaseSettings):
    environment:str = "development"
    model_config = {
        "env_file":".env",
        "extra":"ignore"
    }