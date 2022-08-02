# STANDARD IMPORTS
from unittest.mock import patch, Mock
import pytest

# THIRD PARTY IMPORTS
from persephone_client import Persephone

# PROJECT STUBS
from src.domain.exceptions.exceptions import W8DocumentWasNotUpdated, NotSentToPersephone
from src.domain.models.w8_signature.base.model import W8FormConfirmation
from src.repositories.user.repository import UserRepository
from src.services.w8_signature.service import W8DocumentService

# STUB IMPORTS
from src.transport.onboarding_steps_br.transport import ValidateOnboardingStepsBr
from src.transport.onboarding_steps_us.transport import ValidateOnboardingStepsUS
from tests.src.services.w8_signature.service_stub import payload_w8_sig_stub

get_w8_confirmation_stub = {"unique_id": '40db7fee-6d60-4d73-824f-1bf87edc4491',
                            "w8_form_confirmation": True,
                            }

get_unique_id_from_jwt_payload = "125458.hagfsdsa"

@pytest.mark.asyncio
@patch.object(ValidateOnboardingStepsBr, "validate_onboarding_steps_br", side_effect=[None, None])
@patch.object(ValidateOnboardingStepsUS, "validate_onboarding_steps_us", side_effect=[None, None])
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
@patch.object(UserRepository, "update_one", return_value=True)
async def test_update_w8_form_confirmation_when_sending_right_params_then_return_the_expected(
        mock_onboarding_br_step_validator,
        mock_onboarding_us_step_validator,
        mock_register_user_exchange_member_log,
        mock_update_one
):

    response = await W8DocumentService.update_w8_form_confirmation(
        jwt_data=Mock(return_value=get_unique_id_from_jwt_payload),
        w8_confirmation_request=W8FormConfirmation(**{"w8_confirmation": True})
    )
    assert response is True


@pytest.mark.asyncio
@patch.object(ValidateOnboardingStepsBr, "validate_onboarding_steps_br", side_effect=[None, None])
@patch.object(ValidateOnboardingStepsUS, "validate_onboarding_steps_us", side_effect=[None, None])
@patch.object(Persephone, "send_to_persephone", return_value=[False, False])
@patch.object(UserRepository, "update_one", return_value=True)
async def test_update_w8_form_confirmation_when_sending_right_params_but_not_sent_to_persephone_then_raise_error(
        mock_onboarding_br_step_validator,
        mock_onboarding_us_step_validator,
        mock_register_user_exchange_member_log,
        mock_update_one
):
    with pytest.raises(NotSentToPersephone):
        await W8DocumentService.update_w8_form_confirmation(
            jwt_data=Mock(return_value=get_unique_id_from_jwt_payload),
            w8_confirmation_request=W8FormConfirmation(**{"w8_confirmation": True})
        )


@pytest.mark.asyncio
@patch.object(ValidateOnboardingStepsBr, "validate_onboarding_steps_br", side_effect=[None, None])
@patch.object(ValidateOnboardingStepsUS, "validate_onboarding_steps_us", side_effect=[None, None])
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
@patch.object(UserRepository, "update_one", return_value=False)
async def test_update_w8_form_confirmation_when_sending_right_params_but_not_updating_user_then_raise_error(
        mock_onboarding_br_step_validator,
        mock_onboarding_us_step_validator,
        mock_register_user_exchange_member_log,
        mock_update_one
):
    with pytest.raises(W8DocumentWasNotUpdated):
        await W8DocumentService.update_w8_form_confirmation(
            jwt_data=Mock(return_value=get_unique_id_from_jwt_payload),
            w8_confirmation_request=W8FormConfirmation(**{"w8_confirmation": True})
        )
