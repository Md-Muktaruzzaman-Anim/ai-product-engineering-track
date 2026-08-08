from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    debug: bool
    environment: str

    openai_key: str

    database_url: str

    redis_url: str

    jwt_secret: str

    api_timeout: int = 30