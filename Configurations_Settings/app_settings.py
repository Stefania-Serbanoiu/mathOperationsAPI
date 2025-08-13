from pydantic_settings import BaseSettings
from pydantic import Field


class AppSettings(BaseSettings):
    bearer_token: str = Field(..., alias="BEARER_TOKEN")
    database_url: str = Field(..., alias="DATABASE_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = AppSettings()
