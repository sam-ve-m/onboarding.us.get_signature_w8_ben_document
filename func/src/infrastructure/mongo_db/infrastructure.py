# OUTSIDE LIBRARIES
from motor.motor_asyncio import AsyncIOMotorClient

# PROJECT IMPORTS
from src.infrastructure.env_config import config


class MongoDBInfrastructure:

    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            url = config("MONGO_CONNECTION_URL")
            cls.client = AsyncIOMotorClient(url)
        return cls.client
