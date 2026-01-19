"""Application configuration management using Pydantic v2 settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # Application
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/lunchify"
    database_echo: bool = True

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # API
    api_title: str = "Lunchify Backend"
    api_version: str = "0.1.0"

    # Rate Limiting
    rate_limit_enabled: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"


settings = Settings()
