# STANDARD LIBS
from typing import Optional
from etria_logger import Gladsheim
from datetime import datetime


class MongoDbBaseRepository:
    infra = MongoDBInfrastructure
    cache = RepositoryRedis
    database = None
    collection = None

    @classmethod
    async def update_one(
        cls, old, new, array_filters=None, upsert=False, ttl=60
    ) -> bool:
        if not old or len(old) == 0:
            return False

        if not new or len(new) == 0:
            return False

        try:
            collection = await cls.get_collection()
            Sindri.dict_to_primitive_types(new, types_to_ignore=[datetime])
            await collection.update_one(
                old, {"$set": new}, array_filters=array_filters, upsert=upsert
            )
            if unique_id := new.get("unique_id"):
                await cls._save_cache(query={"unique_id": unique_id}, ttl=ttl, data=new)
            return True
        except Exception as e:
            Gladsheim.error(error=e)
            return False
