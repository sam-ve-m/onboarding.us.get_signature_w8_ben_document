# PROJECT IMPORTS
from heimdall_client import Heimdall, HeimdallStatusResponses
from func.src.domain.exceptions.exceptions import ErrorOnDecodeJwt


class Jwt:
    def __init__(self, jwt: str):
        self.__jwt = jwt

    async def __decode_and_validate_jwt(self):
        jwt_content, heimdall_status_response = await Heimdall.decode_payload(
            jwt=self.__jwt
        )
        if HeimdallStatusResponses.SUCCESS == heimdall_status_response:
            self.__jwt_payload = jwt_content.get("decoded_jwt")
            return self.__jwt_payload
        else:
            raise ErrorOnDecodeJwt()

    def get_unique_id_from_jwt_payload(self):
        return self.__jwt_payload.get("user").get("unique_id")

    def get_w8_confirmation_from_jwt_payload(self):
        return self.__jwt_payload.get("w8_confirmation")

    def get_jwt(self):
        return self.__jwt

    async def __call__(self):
        self.__jwt_payload = await self.__decode_and_validate_jwt()
