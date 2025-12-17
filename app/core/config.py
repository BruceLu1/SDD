from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="CleanFastAPI")
    debug: bool = Field(default=True)
    database_url: str = Field(default="sqlite:///./data/app.db", alias="DATABASE_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()
