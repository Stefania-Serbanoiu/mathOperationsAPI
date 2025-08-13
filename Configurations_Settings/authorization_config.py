from pydantic_settings import BaseSettings
from pydantic import Field


class AuthSettings(BaseSettings):
    bearer_token: str = Field(..., alias="BEARER_TOKEN")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = AuthSettings()
