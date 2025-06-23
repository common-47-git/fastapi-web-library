from os import getenv
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

from pydantic_settings import BaseSettings

# Auth config
SECRET_KEY = str(getenv("SECRET_KEY"))
ALGORITHM = str(getenv("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class DatabaseConfig(BaseSettings):
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


@lru_cache
def get_db_config() -> DatabaseConfig:
    return DatabaseConfig()
