# import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings class for MongoDB connection.

    Attributes:
        MONGODB_URL (str): The URL of the MongoDB server.
        MONGODB_DATABASE (str): The name of the MongoDB database.
        MONGODB_COLLECTION (str): The name of the MongoDB collection.

    """

    MONGODB_URL: str
    MONGODB_DATABASE: str
    MONGODB_COLLECTION: str

    class Config:
        """
        Configuration class for settings.

        Attributes:
            case_sensitive (bool): Specifies whether settings are case-sensitive.
        """
        case_sensitive = True


settings = Settings()
