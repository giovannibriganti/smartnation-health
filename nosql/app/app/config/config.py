import secrets
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DATABASE: str
    MONGODB_COLLECTION: str

    class Config:
        case_sensitive = True


settings = Settings()