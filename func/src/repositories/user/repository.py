# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import UserUniqueIdDoesNotExists
from func.src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure

# STANDARD IMPORTS
from decouple import config

# THIRD PART IMPORTS
from etria_logger import Gladsheim


class UserRepository:
    infra = MongoDBInfrastructure
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::__get_collection::Error when trying to get collection"
            )
            Gladsheim.error(
                error=ex,
                message=message,
                database=cls.database,
                collection=cls.collection,
            )
            raise ex

    @classmethod
    async def update_user_and_us_w8_confirmation(
        cls, unique_id: str, w8_confirmation_request: str
    ):

        user_filter = {"unique_id": unique_id}
        w8_confirmation_query = {
            "$set": {
                "external_exchange_requirements.us.w8_confirmation": w8_confirmation_request
            }
        }

        try:
            collection = await cls.__get_collection()

            user_w8_confirmation_was_updated = await collection.update_one(
                user_filter, w8_confirmation_query
            )

            if user_w8_confirmation_was_updated.matched_count == 0:
                raise UserUniqueIdDoesNotExists()

            return bool(user_w8_confirmation_was_updated)

        except Exception as error:
            Gladsheim.error(error=error)
            return False
