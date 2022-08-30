# STANDARD IMPORTS
import pytest

# PROJECT IMPORTS
from func.src.domain.persephone.template import W8ConfirmationToPersephone


response_stub = {
    "w8_form_confirmation": "True",
    "unique_id": "lalalala"
}


def test_when_sending_right_params_to_w8_form_confirmation_schema_then_return_the_expected():
    response = W8ConfirmationToPersephone.w8_form_confirmation_schema(
        w8_form_confirmation="True",
        unique_id="lalalala"
    )
    assert response == response_stub
    assert isinstance(response, dict)


def test_when_sending_wrong_params_to_w8_form_confirmation_schema_then_raise_error():
    with pytest.raises(TypeError):
        W8ConfirmationToPersephone.w8_form_confirmation_schema(
            w8_form_confirmation="True"
        )
