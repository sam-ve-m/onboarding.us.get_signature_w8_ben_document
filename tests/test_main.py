# STANDARD IMPORTS
from unittest.mock import patch
from flask import Flask
import pytest
from heimdall_client import Heimdall, HeimdallStatusResponses
from werkzeug.test import Headers

# STUB IMPORTS
from func.src.domain.models.jwt.response import Jwt
from tests.main_stub import request_body_stub, decoded_jwt_stub

# PROJECT IMPORTS
from func.main import update_w8_ben
from func.src.services.w8_signature.service import W8DocumentService


get_drive_wealth_id = "125458.hagfsdsa"

response_stub = (b'{"result": null, "message": "update_w8_form_confirmation::sent_to_persephone'
 b':false", "success": false, "code": 88}')


@pytest.mark.asyncio
@patch.object(Jwt, "_Jwt__decode_and_validate_jwt", return_value=get_drive_wealth_id)
@patch.object(Jwt, "get_unique_id_from_jwt_payload", return_value=get_drive_wealth_id)
@patch.object(Jwt, "get_w8_confirmation_from_jwt_payload", return_value=get_drive_wealth_id)
@patch.object(Heimdall, "decode_payload", return_value=(decoded_jwt_stub, HeimdallStatusResponses.SUCCESS))
@patch.object(W8DocumentService, "update_w8_form_confirmation", return_value=True)
async def test_get_w8_ben_when_sending_right_params_then_return_the_expected(
        mock_update_w8_form_confirmation,
        mock_decode_payload,
        mock_get_w8_confirmation_from_jwt_payload,
        mock_get_unique_id_from_jwt_payload,
        mock_decode_and_validate_jwt
):

    app = Flask(__name__)
    with app.test_request_context(
            json=request_body_stub,
            headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        response = await update_w8_ben(request_body=request)
        assert response.data == response_stub


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=(None, HeimdallStatusResponses.INVALID_TOKEN))
@patch.object(Jwt, "get_unique_id_from_jwt_payload", return_value=get_drive_wealth_id)
@patch.object(Jwt, "get_w8_confirmation_from_jwt_payload", return_value=get_drive_wealth_id)
@patch.object(W8DocumentService, "update_w8_form_confirmation", return_value=True)
async def test_get_w8_ben_when_sending_wrong_params_then_return_the_expected_which_is_invalid_params_error(
        mock_decode_and_validate_jwt,
        mock_get_unique_id_from_jwt_payload,
        mock_get_w8_confirmation_from_jwt_payload,
        mock_update_w8_form_confirmation
):
    app = Flask(__name__)
    with app.test_request_context(
            json=None,
            headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        with pytest.raises(Exception):
            await update_w8_ben(
                request_body=None
            )
