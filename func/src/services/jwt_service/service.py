# THIRD PARTY IMPORTS
from etria_logger import Gladsheim
from heimdall_client import Heimdall

# PROJECT IMPORTS
from heimdall_client.src.domain.enums.heimdall_status_responses import HeimdallStatusResponses
from func.src.domain.exceptions.exceptions import ErrorOnDecodeJwt


class JWTService:

    @classmethod
    async def decode_jwt_from_request(cls, jwt_data: str):
        try:
            jwt_content, heimdall_status_response = await Heimdall.decode_payload(jwt=jwt_data)
            if HeimdallStatusResponses.SUCCESS == heimdall_status_response:
                payload = jwt_content.get("decoded_jwt")
                return payload
            raise ErrorOnDecodeJwt

        except Exception as error:
            message = "JwtService::decode_jwt_and_get_unique_id::Failed to decode JWT"
            Gladsheim.error(error=error, message=message)
            raise error
