from typing import Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URL: str
    INTERVAL: int = 60

    SOURCE_URL: str
    SOURCE_USERNAME: Optional[str] = None
    SOURCE_PASSWORD: Optional[str] = None
