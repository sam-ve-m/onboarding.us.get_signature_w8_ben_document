# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# THIRD PARTY IMPORTS
from persephone_client import Persephone

# PROJECT STUBS
from src.domain.exceptions.exceptions import WasNotSentToPersephone, W8DocumentWasNotUpdated
from src.domain.persephone.template import GetW8ConfirmationTemplate
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import UserOnBoardingStepsService
from src.services.w8_signature.service import W8DocumentService

# STUB IMPORTS
from tests.src.services.w8_signature.service_stub import payload_w8_sig_stub

get_w8_confirmation_stub = {"unique_id": '40db7fee-6d60-4d73-824f-1bf87edc4491',
                            "w8_form_confirmation": True,
                            }


@pytest.mark.asyncio
@patch.object(UserOnBoardingStepsService, "onboarding_br_step_validator", return_value=None)
@patch.object(UserOnBoardingStepsService, "onboarding_us_step_validator", return_value=None)
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
@patch.object(GetW8ConfirmationTemplate,
              "get_w8_form_confirmation_schema_template_with_data",
              return_value=[get_w8_confirmation_stub])
@patch.object(UserRepository, "update_one", return_value=True)
async def test_update_w8_form_confirmation_when_sending_right_params_then_return_the_expected(
        mock_update_one,
        mock_get_w8_form_confirmation_schema_template_with_data,
        mock_send_to_persephone,
        mock_onboarding_us_step_validator,
        mock_onboarding_br_step_validator
):

    response = await W8DocumentService.update_w8_form_confirmation(
        payload=payload_w8_sig_stub
    )
    assert response is True


@pytest.mark.asyncio
@patch.object(UserOnBoardingStepsService, "onboarding_br_step_validator", return_value=None)
@patch.object(UserOnBoardingStepsService, "onboarding_us_step_validator", return_value=None)
@patch.object(Persephone, "send_to_persephone", return_value=[False, False])
@patch.object(GetW8ConfirmationTemplate,
              "get_w8_form_confirmation_schema_template_with_data",
              return_value=[get_w8_confirmation_stub])
async def test_update_w8_form_confirmation_when_sending_right_params_but_not_sent_to_persephone_then_raise_error(
        mock_get_w8_form_confirmation_schema_template_with_data,
        mock_send_to_persephone,
        mock_onboarding_us_step_validator,
        mock_onboarding_br_step_validator
):
    with pytest.raises(WasNotSentToPersephone):
        await W8DocumentService.update_w8_form_confirmation(
            payload=payload_w8_sig_stub
        )


@pytest.mark.asyncio
@patch.object(UserOnBoardingStepsService, "onboarding_br_step_validator", return_value=None)
@patch.object(UserOnBoardingStepsService, "onboarding_us_step_validator", return_value=None)
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
@patch.object(GetW8ConfirmationTemplate,
              "get_w8_form_confirmation_schema_template_with_data",
              return_value=[get_w8_confirmation_stub])
@patch.object(UserRepository, "update_one", return_value=False)
async def test_update_w8_form_confirmation_when_sending_right_params_but_not_updating_user_then_raise_error(
        mock_update_one,
        mock_get_w8_form_confirmation_schema_template_with_data,
        mock_send_to_persephone,
        mock_onboarding_us_step_validator,
        mock_onboarding_br_step_validator
):
    with pytest.raises(W8DocumentWasNotUpdated):
        await W8DocumentService.update_w8_form_confirmation(
            payload=payload_w8_sig_stub
        )
