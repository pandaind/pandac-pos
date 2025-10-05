from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = Field(default="Pandac POS API", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    api_v1_str: str = Field(default="/v1", env="API_V1_STR")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_url_test: Optional[str] = Field(default=None, env="DATABASE_URL_TEST")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS
    backend_cors_origins: List[str] = Field(default=[], env="BACKEND_CORS_ORIGINS")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Celery
    celery_broker_url: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/0", env="CELERY_RESULT_BACKEND")
    
    # Email (optional)
    smtp_tls: bool = Field(default=True, env="SMTP_TLS")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_host: Optional[str] = Field(default=None, env="SMTP_HOST")
    smtp_user: Optional[str] = Field(default=None, env="SMTP_USER")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
