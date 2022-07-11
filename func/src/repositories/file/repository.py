# STANDARD LIBS
from base64 import b64decode, b64encode
from enum import Enum
from io import BytesIO
from typing import Union, Optional
from aiohttp import ClientSession


# OUTSIDE LIBRARIES
from func.src.domain.exceptions.exceptions import InternalServerError
from func.src.infrastructure.s3.infrastructure import S3Infrastructure
from func.src.repositories.cache.repository import RepositoryRedis
from func.src.repositories.file.enum.term_file import TermsFileType
from func.src.repositories.file.enum.user_file import UserFileType


class FileRepository:

    infra = S3Infrastructure
    cache = RepositoryRedis

    # This dict keys must be TermsFileType, UserFileType constants
    _file_extension_by_type = {
        "user_selfie": ".jpg",
        "document_front": ".jpg",
        "document_back": ".jpg",
        "term_application": ".pdf",
        "term_open_account": ".pdf",
        "term_refusal": ".pdf",
        "term_non_compliance": ".pdf",
        "term_retail_liquid_provider": ".pdf",
        "term_open_account_dw": ".pdf",
        "term_application_dw": ".pdf",
        "term_and_privacy_policy_data_sharing_policy_dw": ".pdf",
        "term_disclosures_and_disclaimers": ".pdf",
        "term_money_corp": ".pdf",
        "term_gringo_world": ".pdf",
        "term_gringo_world_general_advices": ".pdf",
    }

    @classmethod
    async def save_user_file(
        cls,
        file_type: UserFileType,
        content: Union[str, bytes],
        unique_id: str,
        bucket_name: str,
    ) -> str:
        path = await cls._resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = cls._get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        fully_qualified_path = f"{path}{file_name}{file_extension}"
        async with cls.infra.get_client() as s3_client:
            await s3_client.upload_fileobj(
                cls._resolve_content(content=content),
                bucket_name,
                fully_qualified_path,
            )
        return fully_qualified_path

    @classmethod
    async def get_user_file(
        cls,
        file_type: UserFileType,
        unique_id: str,
        bucket_name: str,
    ) -> Union[str, dict]:
        path = await cls._resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = cls._get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        fully_qualified_path = f"{path}{file_name}{file_extension}"
        url = None
        async with cls.infra.get_client() as s3_client:
            url = await s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": fully_qualified_path},
                ExpiresIn=604800,
            )
        return url

    @classmethod
    async def get_file_as_base_64(
        cls,
        file_type: UserFileType,
        unique_id: str,
        bucket_name: str,
    ) -> str:
        url = await cls.get_user_file(
            file_type=file_type, unique_id=unique_id, bucket_name=bucket_name
        )
        if url is None:
            raise InternalServerError("files.error")
        async with ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    byte_content = await response.read()
                    base_64_content = b64encode(byte_content).decode()
                    return f"data:image/jpeg;base64,{base_64_content}"
                raise InternalServerError("files.error")

    @classmethod
    async def user_file_exists(
        cls, file_type: UserFileType, unique_id: str, bucket_name: str
    ):
        prefix = await cls._resolve_user_path(unique_id=unique_id, file_type=file_type)
        file_name = file_type.value
        file_extension = cls._get_file_extension_by_type(file_type=file_type)
        if not prefix or not file_name or not file_extension:
            raise InternalServerError("files.error")

        objects = None
        async with cls.infra.get_resource() as s3_resource:
            bucket = await s3_resource.Bucket(bucket_name)
            async for s3_object in bucket.objects.filter(Prefix=prefix):
                objects = s3_object

        if not objects:
            exists_selfie = False
        else:
            exists_selfie = True

        return exists_selfie

    @classmethod
    async def save_term_file(
        cls, file_type: TermsFileType, content: Union[str, bytes], bucket_name: str
    ) -> None:
        path = cls._resolve_term_path(file_type=file_type)
        current_version = await cls.get_current_term_version(
            file_type=file_type, bucket_name=bucket_name
        )
        new_version = current_version + 1
        file_name = cls._generate_term_file_name(
            name=file_type.value, version=new_version
        )
        file_extension = cls._get_file_extension_by_type(file_type=file_type)
        if not path or not file_name or not file_extension:
            raise InternalServerError("files.error")
        async with cls.infra.get_client() as s3_client:
            await s3_client.upload_fileobj(
                cls._resolve_content(content),
                bucket_name,
                f"{path}{file_name}{file_extension}",
            )
        return

    @classmethod
    async def get_term_file(
        cls, file_type: TermsFileType, bucket_name: str, ttl: int = 3600
    ) -> Union[str, dict]:
        cache_key = f"get_term_file:{file_type.value}"
        cached_value = await cls.cache.get(key=cache_key)
        if cached_value:
            return cached_value
        path = cls._resolve_term_path(file_type=file_type)
        try:
            file_path = await cls._get_last_saved_file_from_folder(
                path=path, bucket_name=bucket_name
            )
        except InternalServerError:
            return
        else:
            if not file_path:
                return
            url = None
            async with cls.infra.get_client() as s3_client:
                url = await s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket_name, "Key": file_path},
                    ExpiresIn=ttl,
                )
            await cls.cache.set(key=cache_key, value=url, ttl=ttl)
            return url

    @classmethod
    async def get_terms_version(cls, bucket_name: str) -> dict:
        value = dict()
        for file_type in TermsFileType:
            version = await cls.get_current_term_version(
                file_type=file_type, bucket_name=bucket_name
            )
            value.update({file_type.value: version})
        return value

    @classmethod
    async def get_term_file_by_version(
        cls, file_type: TermsFileType, version: int, bucket_name: str, ttl: int = 3600
    ) -> str:
        file_name = cls._generate_term_file_name(name=file_type.value, version=version)
        path = cls._resolve_term_path(file_type=file_type)
        file_extension = cls._get_file_extension_by_type(file_type=file_type)
        url = None
        async with cls.infra.get_client() as s3_client:
            url = await s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket_name,
                    "Key": f"{path}{file_name}{file_extension}",
                },
                ExpiresIn=ttl,
            )
        return url

    @classmethod
    async def get_current_term_version(
        cls, file_type: TermsFileType, bucket_name: str
    ) -> int:
        version = 0
        async with cls.infra.get_resource() as s3_resource:
            bucket = await s3_resource.Bucket(bucket_name)
            prefix = cls._resolve_term_path(file_type=file_type)
            async for s3_object in bucket.objects.filter(Prefix=prefix, Delimiter="/"):
                version += 1
        return version

    @staticmethod
    def _generate_term_file_name(name: str, version: int):
        if version is None or name is None:
            raise InternalServerError("files.params.invalid")
        return f"{name}_v{version}"

    @staticmethod
    def _resolve_term_path(file_type: TermsFileType) -> str:
        return f"{file_type.value}/"

    @classmethod
    def _get_file_extension_by_type(cls, file_type: Enum) -> Optional[str]:
        valid_files = list()
        for file_enum in [UserFileType, TermsFileType]:
            valid_files += [item.value for item in file_enum]
        if file_type.value not in valid_files:
            raise InternalServerError("files.error")
        return cls._file_extension_by_type.get(file_type.value)

    @staticmethod
    async def _resolve_user_path(unique_id: str, file_type: UserFileType) -> str:
        return f"{unique_id}/{file_type.value}/"

    @classmethod
    async def _get_last_saved_file_from_folder(
        cls, path: str, bucket_name: str
    ) -> Optional[str]:
        if type(path) is not str:
            raise InternalServerError("files.error")

        objects = list()
        async with cls.infra.get_resource() as s3_resource:
            bucket = await s3_resource.Bucket(bucket_name)
            async for s3_object in bucket.objects.filter(Prefix=path, Delimiter="/"):
                objects.append(s3_object)

        objects.reverse()

        if not len(objects) > 0:
            raise InternalServerError("files.is_empty")

        latest_file = objects[0]
        file_key = latest_file.key
        return file_key

    @staticmethod
    def _resolve_content(content: Union[str, bytes]) -> BytesIO:
        """str in this case is a base64 string"""
        if content is None:
            raise InternalServerError("files.content.empty")
        if type(content) is str:
            base64_bytes = content.encode("ascii")
            content = b64decode(base64_bytes)
        bytes_io = BytesIO()
        bytes_io.write(content)
        bytes_io.seek(0)
        return bytes_io
