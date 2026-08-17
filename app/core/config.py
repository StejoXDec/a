from __future__ import annotations

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'SegarChain API'
    database_url: str = 'sqlite:///./segarchain.db'
    cors_origins: str = '*'
    discount_rate: float = 0.25
    default_radius_km: float = 25.0

    class Config:
        env_file = '.env'
        case_sensitive = False


settings = Settings()


class AppConfig(BaseModel):
    app_name: str = settings.app_name
    database_url: str = settings.database_url
    cors_origins: str = settings.cors_origins
    discount_rate: float = settings.discount_rate
    default_radius_km: float = settings.default_radius_km
