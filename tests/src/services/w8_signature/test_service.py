# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# THIRD PARTY IMPORTS
from persephone_client import Persephone

# PROJECT STUBS
from src.domain.persephone.model import GetW8ConfirmationTemplate
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import UserOnBoardingStepsService
from src.services.w8_signature.service import W8DocumentService
from tests.src.services.w8_signature.service_stub import payload_w8_sig_stub

get_w8_confirmation_stub = {"unique_id": '40db7fee-6d60-4d73-824f-1bf87edc4491',
                            "w8_form_confirmation": True,
                            }


@pytest.mark.asyncio
@patch.object(UserOnBoardingStepsService, "onboarding_br_step_validator", return_value=None)
@patch.object(UserOnBoardingStepsService, "onboarding_us_step_validator", return_value=None)
@patch.object(Persephone, "send_to_persephone", return_value=True)
@patch.object(GetW8ConfirmationTemplate,
              "get_w8_form_confirmation_schema_template_with_data",
              return_value=get_w8_confirmation_stub)
@patch.object(UserRepository, "update_one", return_value=True)
async def test_update_w8_form_confirmation_when_sending_right_params_then_return_the_expected(
    mock_onboarding_br_step_validator,
    mock_onboarding_us_step_validator,
    mock_send_to_persephone,
    mock_get_w8_form_confirmation_schema_template_with_data,
    mock_update_one
):
    response = await W8DocumentService.update_w8_form_confirmation(
        payload=payload_w8_sig_stub
    )
    assert response is True
