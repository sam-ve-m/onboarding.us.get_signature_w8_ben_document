from unittest.mock import patch

import pytest
from decouple import Config
from etria_logger import Gladsheim
from flask import Flask
from heimdall_client import Heimdall, HeimdallStatusResponses
from werkzeug.test import Headers

with patch.object(Config, "__call__"):
    from func.main import update_w8_ben
    from func.src.domain.models.jwt.response import Jwt
    from func.src.services.w8_signature.service import W8DocumentService
    from func.src.domain.exceptions.exceptions import (
        DeviceInfoNotSupplied,
        DeviceInfoRequestFailed,
    )
    from func.src.transport.device_info.transport import DeviceSecurity
    from tests.main_stub import request_body_stub, decoded_jwt_stub

get_drive_wealth_id = "125458.hagfsdsa"

response_stub = (
    b'{"result": true, "message": "The W8 Form Was Updated Successfully", "success'
    b'": true, "code": 0}'
)


@pytest.mark.asyncio
@patch.object(Jwt, "_Jwt__decode_and_validate_jwt", return_value=get_drive_wealth_id)
@patch.object(Jwt, "get_unique_id_from_jwt_payload", return_value=get_drive_wealth_id)
@patch.object(
    Jwt, "get_w8_confirmation_from_jwt_payload", return_value=get_drive_wealth_id
)
@patch.object(
    Heimdall,
    "decode_payload",
    return_value=(decoded_jwt_stub, HeimdallStatusResponses.SUCCESS),
)
@patch(
    "func.src.services.w8_signature.service.W8DocumentService.update_w8_form_confirmation",
    return_value=True,
)
@patch.object(DeviceSecurity, "get_device_info")
@patch.object(Config, "__call__")
async def test_get_w8_ben_when_sending_right_params_then_return_the_expected(
    config,
    device_info,
    mock_update_w8_form_confirmation,
    mock_decode_payload,
    mock_get_w8_confirmation_from_jwt_payload,
    mock_get_unique_id_from_jwt_payload,
    mock_decode_and_validate_jwt,
):
    app = Flask(__name__)
    with app.test_request_context(
        json=request_body_stub,
        headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        response = await update_w8_ben(request=request)
        assert response.data == response_stub


#
#
@pytest.mark.asyncio
@patch.object(
    Heimdall,
    "decode_payload",
    return_value=(None, HeimdallStatusResponses.INVALID_TOKEN),
)
@patch.object(Jwt, "get_unique_id_from_jwt_payload", return_value=get_drive_wealth_id)
@patch.object(
    Jwt, "get_w8_confirmation_from_jwt_payload", return_value=get_drive_wealth_id
)
@patch.object(W8DocumentService, "update_w8_form_confirmation", return_value=True)
@patch.object(DeviceSecurity, "get_device_info")
@patch.object(Config, "__call__")
async def test_get_w8_ben_when_sending_wrong_params_then_return_the_expected_which_is_invalid_params_error(
    config,
    device_info,
    mock_decode_and_validate_jwt,
    mock_get_unique_id_from_jwt_payload,
    mock_get_w8_confirmation_from_jwt_payload,
    mock_update_w8_form_confirmation,
):
    app = Flask(__name__)
    with app.test_request_context(
        json=None,
        headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        device_info.side_effect = Exception()
        response = await update_w8_ben(request)
        assert response.status_code == 500


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(Heimdall, "decode_payload")
@patch.object(W8DocumentService, "update_w8_form_confirmation")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_employ_for_us_when_fail_to_get_device_info(
    device_info,
    update_w8_confirmation,
    heimdall_mock,
    etria_mock,
):
    update_w8_confirmation.side_effect = DeviceInfoRequestFailed("errooou")
    heimdall_mock.return_value = ({}, HeimdallStatusResponses.SUCCESS)
    app = Flask(__name__)
    with app.test_request_context(
        json=request_body_stub,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_w8_ben(request)

        assert (
            result.data
            == b'{"result": null, "message": "Error trying to get device info", "success": false, "code": 100}'
        )
        assert etria_mock.called


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(Heimdall, "decode_payload")
@patch.object(W8DocumentService, "update_w8_form_confirmation")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_employ_for_us_when_device_info_is_not_supplied(
    device_info,
    update_w8_confirmation,
    heimdall_mock,
    etria_mock,
):
    update_w8_confirmation.side_effect = DeviceInfoNotSupplied("errooou")
    heimdall_mock.return_value = ({}, HeimdallStatusResponses.SUCCESS)
    app = Flask(__name__)
    with app.test_request_context(
        json=request_body_stub,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_w8_ben(request)

        assert (
            result.data
            == b'{"result": null, "message": "Device info not supplied", "success": false, "code": 10}'
        )
        assert etria_mock.called
