import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP: str = os.getenv("APPLICATION_APP")
    HOST: str = os.getenv("APPLICATION_HOST", "0.0.0.0")
    PORT: int = os.getenv("APPLICATION_PORT", 8080)
    DEBUG: bool = os.getenv("APPLICATION_DEBUG", False)

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    DB_HOST: str = os.getenv("POSTGRES_HOST")
    DB_PORT: int = os.getenv("POSTGRES_PORT")
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_NAME: str = os.getenv("POSTGRES_DB")

settings = Settings()
