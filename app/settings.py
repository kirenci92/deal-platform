from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    POSTGRES_DB: str = "deal_platform"
    POSTGRES_USER: str = "dealuser"
    POSTGRES_PASSWORD: str = "dealpassword"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    TELEGRAM_TOKEN: str = ""
    TELEGRAM_CHANNEL: str = ""

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
