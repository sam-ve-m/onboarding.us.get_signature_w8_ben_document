# STANDARD IMPORTS
from unittest.mock import patch
from flask import Flask
import pytest
from werkzeug.exceptions import BadRequest
from werkzeug.test import Headers

# STUB IMPORTS
from main import update_w8_ben_signature
from main_stub import decoded_jwt_stub, request_body_stub, response_bytes_stub

# PROJECT IMPORTS
from src.services.jwt_service.service import JWTService
from src.services.w8_signature.service import W8DocumentService


@pytest.mark.asyncio
@patch.object(JWTService, "decode_jwt_from_request", return_value=decoded_jwt_stub)
@patch.object(W8DocumentService, "update_w8_form_confirmation", return_value=True)
async def test_get_w8_ben_when_sending_right_params_then_return_the_expected(
        mock_decode_jwt_from_request,
        mock_update_w8_form_confirmation
):
    app = Flask(__name__)
    with app.test_request_context(
            json=request_body_stub,
            headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        response = await update_w8_ben_signature(request_body=request)
        assert response.data == response_bytes_stub


@pytest.mark.asyncio
@patch.object(JWTService, "decode_jwt_from_request", return_value=decoded_jwt_stub)
@patch.object(W8DocumentService, "update_w8_form_confirmation", return_value=True)
async def test_get_w8_ben_when_sending_wrong_params_then_return_the_expected_which_is_invalid_params_error(
        mock_decode_jwt_from_request,
        mock_update_w8_form_confirmation
):
    app = Flask(__name__)
    with app.test_request_context(
            json=None,
            headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        with pytest.raises(BadRequest):
            await update_w8_ben_signature(request_body=request)
