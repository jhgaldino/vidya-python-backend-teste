from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sales API"
    sqlite_url: str = "sqlite:///./data/sales.db"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "sales_db"
    mongo_collection_name: str = "sale_texts"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

