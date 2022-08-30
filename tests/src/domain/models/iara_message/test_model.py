# STANDARD IMPORTS
import pytest

# PROJECT IMPORTS
from func.src.domain.models.iara_message.model import IaraMessage


response_stub = {
    "unique_id": "lalalalalala"
}


def test_when_sending_right_params_to_user_w8_signature_iara_schema_then_return_the_expected():
    response = IaraMessage.user_w8_signature_iara_schema(
        unique_id="lalalalalala"
    )
    assert response == response_stub


def test_when_sending_wrong_params_to_user_w8_signature_iara_schema_then_raise_exception():
    with pytest.raises(TypeError):
        IaraMessage.user_w8_signature_iara_schema()
