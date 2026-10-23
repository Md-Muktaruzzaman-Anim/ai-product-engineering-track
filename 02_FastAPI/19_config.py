from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    database_url: str
    jwt_secret: str
    openai_api_key: str

    redis_url: str = (
        "redis://localhost:6379"
    )

    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


if __name__ == "__main__":

    settings = get_settings()

    print(
        "Database:",
        settings.database_url,
    )

    print(
        "Redis:",
        settings.redis_url,
    )