from typing import Optional

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    _USE_PYDANTIC = True
except ImportError:
    _USE_PYDANTIC = False
    class BaseSettings:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    SettingsConfigDict = dict


class Settings(BaseSettings):
    APP_NAME: str = "Cloud-Native Order Service"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8081
    HOST: str = "0.0.0.0"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/orders"
    TAX_RATE: float = 0.08  # 8% default sales tax

    if _USE_PYDANTIC:
        model_config = SettingsConfigDict(
            env_file=".env",
            case_sensitive=False,
            extra="ignore",
        )


settings = Settings()
