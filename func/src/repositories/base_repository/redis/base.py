# STANDARD IMPORTS
from typing import Union
import pickle

# PROJECT IMPORT
from src.domain.exceptions.exceptions import InternalServerError
from src.infrastructure.redis.infrastructure import RedisInfrastructure


class BaseRepositoryRedis(RedisInfrastructure):
    prefix = ""

    @classmethod
    async def get(cls, key: str) -> Union[dict, str, bytes]:
        redis = cls.get_redis()
        if type(key) != str:
            raise InternalServerError("cache.error.key")
        key = f"{cls.prefix}{key}"
        value = await redis.get(name=key)
        return value and pickle.loads(value) or value

    @classmethod
    async def set(cls, key: str, value: dict, ttl: int = 0) -> None:
        redis = cls.get_redis()
        """ttl in secounds"""
        key = f"{cls.prefix}{key}"
        if ttl > 0:
            await redis.set(name=key, value=pickle.dumps(value), ex=ttl)
        else:
            await redis.set(name=key, value=pickle.dumps(value))
