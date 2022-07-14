# PROJECT IMPORTS
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository

# STANDARD IMPORTS
from decouple import config


class UserRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")
