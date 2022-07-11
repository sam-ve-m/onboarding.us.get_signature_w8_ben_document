# STANDARD LIBS
from typing import Optional
from etria_logger import Gladsheim
from datetime import datetime

# OUTSIDE LIBRARIES
from pymongo.cursor import Cursor
from nidavellir import Sindri

# Sphinx
from func.src.domain.model_decorator.generate_id import hash_field
from func.src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure
from func.src.repositories.cache.repository import RepositoryRedis


class MongoDbBaseRepository:
    infra = MongoDBInfrastructure
    cache = RepositoryRedis
    database = None
    collection = None

    @classmethod
    def get_base_identifier(cls):
        if not (cls.database and cls.collection):
            raise Exception(
                "The gods think you are a foolish guy because you don't know what you want. Try again!"
            )
        return f"{cls.database}:{cls.collection}"

    @classmethod
    async def get_collection(cls):
        if not (cls.database and cls.collection):
            raise Exception(
                "The gods think you are a foolish guy because you don't know what you want. Try again!"
            )
        mongo_client = cls.infra.get_client()
        database = mongo_client[cls.database]
        collection = database[cls.collection]
        return collection

    @classmethod
    async def insert(cls, data: dict) -> bool:
        try:
            collection = await cls.get_collection()
            await collection.insert_one(data)
            return True
        except Exception as e:
            Gladsheim.error(error=e)
            return False

    @classmethod
    async def find_one(
        cls, query: dict, ttl: int = None, project: dict = None
    ) -> Optional[dict]:
        if ttl is None:
            ttl = 0
        try:
            collection = await cls.get_collection()
            data = None

            has_ttl = ttl > 0  # pragma: no cover
            if has_ttl:  # pragma: no cover
                data = await cls._get_from_cache(query=query)

            if not data:  # pragma: no cover
                data = await collection.find_one(query, project)

            if has_ttl and data is not None:  # pragma: no cover
                await cls._save_cache(query=query, ttl=ttl, data=data)

            return data

        except Exception as e:
            Gladsheim.error(error=e)
            raise Exception("internal_error")

    @classmethod
    async def find_all(
        cls, query: dict, project: dict = None, sort: tuple = None, limit: int = None
    ) -> Optional[Cursor]:
        try:
            if query is None:
                query = {}
            collection = await cls.get_collection()
            query = collection.find(query, project)
            if sort:
                query.sort(*sort)
            return await query.to_list(limit)
        except Exception as e:
            Gladsheim.error(error=e)
            raise Exception("internal_error")

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

    @classmethod
    async def add_one_in_array(
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
                old, {"$push": new}, array_filters=array_filters, upsert=upsert
            )
            return True
        except Exception as e:
            Gladsheim.error(error=e)
            return False

    @classmethod
    async def delete_one_in_array(
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
                old, {"$pull": new}, array_filters=array_filters, upsert=upsert
            )
            return True
        except Exception as e:
            Gladsheim.error(error=e)
            return False

    @classmethod
    async def delete_one(cls, entity, ttl=0) -> bool:
        try:
            collection = await cls.get_collection()
            await collection.delete_one(entity)
            if unique_id := entity.get("unique_id"):  # pragma: no cover
                await cls._delete_cache(query={"unique_id": unique_id})
            return True
        except Exception as e:
            Gladsheim.error(error=e)
            return False

    @classmethod
    async def _get_from_cache(cls, query: dict):
        if query is None:
            return None
        query_hash = await hash_field(payload=query)
        base_identifier = cls.get_base_identifier()
        cache_value = await cls.cache.get(key=f"{base_identifier}:{query_hash}")
        if cache_value:
            return cache_value
        return None

    @classmethod
    async def _save_cache(cls, data: dict, query: dict, ttl: int = 0):

        ttl = 60 if ttl == 0 else ttl  # pragma: no cover

        query_hash = await hash_field(payload=query)
        base_identifier = cls.get_base_identifier()
        await cls.cache.set(
            key=f"{base_identifier}:{query_hash}",
            value=data,
            ttl=ttl,
        )

    @classmethod
    async def _delete_cache(cls, query: dict):
        query_hash = await hash_field(payload=query)
        await cls.cache.delete(key=query_hash)
