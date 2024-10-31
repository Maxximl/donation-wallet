from os import environ, makedirs
from os.path import abspath, dirname, join

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api")
    APP_HOST: str = environ.get("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(environ.get("APP_PORT", "8000"))
    STATIC_FILES_PATH: str = environ.get("STATIC_FILES_PATH", "/tmp/static")

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "test")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "test")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "test")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432"))
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "test")

    # to get a string like this run: "openssl rand -hex 32"
    SECRET_KEY: str = environ.get("SECRET_KEY", "")
    ALGORITHM: str = environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    )
    AUTH_HOST: str = APP_HOST
    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl=f"{PATH_PREFIX}/authentication"
    )

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings():
    return DefaultSettings()
