# OUTSIDE LIBRARIES
import aioboto3
from contextlib import asynccontextmanager
from etria_logger import Gladsheim

# Sphinx
from func.src.domain.exceptions.exceptions import InternalServerError
from func.src.infrastructure.env_config import config


class S3Infrastructure:

    session = None

    @classmethod
    async def _get_session(cls):
        if cls.session is None:
            cls.session = aioboto3.Session(
                aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
                region_name=config("REGION_NAME"),
            )
        return cls.session

    @classmethod
    @asynccontextmanager
    async def get_client(cls):
        try:
            session = await S3Infrastructure._get_session()
            async with session.client("s3") as s3_client:
                yield s3_client
        except Exception as e:
            Gladsheim.error(error=e)
            raise InternalServerError("files.error")

    @classmethod
    @asynccontextmanager
    async def get_resource(cls):
        try:
            session = await S3Infrastructure._get_session()
            async with session.resource("s3") as s3_resource:
                yield s3_resource
        except Exception as e:
            Gladsheim.error(error=e)
            raise InternalServerError("files.error")

    @classmethod
    @asynccontextmanager
    async def get_bucket(cls, bucket_name: str):
        try:
            if cls.session is None:
                cls.session = aioboto3.Session()
            async with cls.session.resource(
                "s3",
                aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
                region_name=config("REGION_NAME"),
            ) as s3:
                bucket = await s3.Bucket(bucket_name)
                yield bucket
        except Exception as e:
            Gladsheim.error(error=e)
            raise InternalServerError("files.error")
