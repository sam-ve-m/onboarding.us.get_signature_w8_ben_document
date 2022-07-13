# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# THIRD PARTY IMṔORTS
from heimdall_client import Heimdall, HeimdallStatusResponses

# PROJECT IMPORTS
from src.services.jwt_service.service import JWTService

# STUB IMPORTS
from tests.src.services.jwt_service.service_stub import jwt_data_stub, jwt_to_decode_stub, decoded_jwt_stub


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=(jwt_data_stub, HeimdallStatusResponses.SUCCESS))
async def test_when_sending_right_params_to_the_function_then_return_the_expected(
        mock_decode_payload
):
    response = await JWTService.decode_jwt_from_request(
        jwt_data=jwt_to_decode_stub
    )
    assert response == decoded_jwt_stub


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=(None, HeimdallStatusResponses.INVALID_TOKEN))
async def test_when_sending_right_params_to_the_function_then_return_the_expected(
        mock_decode_payload
):
    with pytest.raises(Exception):
        await JWTService.decode_jwt_from_request(
            jwt_data=jwt_to_decode_stub
        )
