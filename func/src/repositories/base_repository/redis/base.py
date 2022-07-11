from src.exceptions.exceptions import InternalServerError
from src.infrastructures.redis.infrastructure import RedisInfrastructure
from typing import Union, Optional
import pickle


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
