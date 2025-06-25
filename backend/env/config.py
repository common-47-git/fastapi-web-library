from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


class DatabaseConfig(BaseConfig):
    LOGIN_USER: str
    PASSWORD: str
    SERVERNAME: str
    DBNAME: str
    DRIVER: str

    @property
    def pg_dsn(self) -> str:
        return (
            f"postgresql+{self.DRIVER}://{self.LOGIN_USER}:{self.PASSWORD}"
            f"@{self.SERVERNAME}/{self.DBNAME}"
        )


class AuthConfig(BaseConfig):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


@lru_cache
def get_db_config() -> DatabaseConfig:
    return DatabaseConfig()


@lru_cache
def get_auth_config() -> AuthConfig:
    return AuthConfig()
