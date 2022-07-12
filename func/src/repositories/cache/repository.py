# PROJECT IMPORTS
from func.src.infrastructure.env_config import config
from func.src.repositories.base_repository.redis.base import BaseRepositoryRedis


class RepositoryRedis(BaseRepositoryRedis):
    redis_host = config("REDIS_HOST_URL")
    redis_db = config("REDIS_CACHE_DB")
    prefix = "sphinx:"
