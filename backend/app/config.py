from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Orqis"
    debug: bool = False
    api_prefix: str = "/api"

    arango_url: str = "http://localhost:8529"
    arango_db: str = "orqis"
    arango_user: str = "root"
    arango_password: str = "orqis_dev_password"

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080

    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "orqis-mvp"

    mock_agents: bool = True
    openai_api_key: str | None = None

    seed_dev_user: bool = False
    dev_user_email: str = "dev@orqis.local"
    dev_user_password: str = "devpassword"

    execution_output_max_bytes: int = 262144
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()
