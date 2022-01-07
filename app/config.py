from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_PREFIX = "/api/v1"
    APP_NAME = "Inventory Management API"
    MONGO_URI: str
    TEST_COLLECTION = "TEST_DATABASE"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
