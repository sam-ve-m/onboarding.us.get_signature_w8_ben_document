# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import UserUniqueIdDoesNotExists, InvalidOnboardingStep
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import UserOnBoardingStepsService

# STUBS
from tests.src.services.on_boarding_steps.service_stub import find_one_stub_steps, builder_stub_on_boarding_steps, \
    builder_stub_us_onbording, onboarding_user_current_step_us_stub, onboarding_user_invalid_current_step_us_stub


@pytest.mark.asyncio
@patch.object(FileRepository, "user_file_exists", side_effect=[True, True, True, True])
@patch.object(UserRepository, "find_one", return_value=find_one_stub_steps)
async def test_on_boarding_user_current_step_br_when_sending_right_params_the_return_the_expected(
        mock_find_one,
        mock_user_file_exists,
):
    response = await UserOnBoardingStepsService.onboarding_user_current_step_br(
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491"
    )
    assert response == builder_stub_on_boarding_steps
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch.object(FileRepository, "user_file_exists", side_effect=[True, True, True, True])
@patch.object(UserRepository, "find_one", return_value=None)
async def test_on_boarding_user_current_step_br_when_current_user_is_none_the_raise_unique_id_doesnt_exists_error(
        mock_find_one,
        mock_user_file_exists,
):
    with pytest.raises(UserUniqueIdDoesNotExists):
        await UserOnBoardingStepsService.onboarding_user_current_step_br(
            unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491"
        )


@pytest.mark.asyncio
@patch.object(FileRepository, "user_file_exists", side_effect=[True, True, True, True])
@patch.object(UserRepository, "find_one", return_value=find_one_stub_steps)
async def test_onboarding_user_current_step_us_when_sending_right_params_the_return_the_expected(
        mock_find_one,
        mock_user_file_exists,
):
    response = await UserOnBoardingStepsService.onboarding_user_current_step_us(
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491"
    )
    assert response == builder_stub_us_onbording
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch.object(FileRepository, "user_file_exists", side_effect=[True, True, True, True])
@patch.object(UserRepository, "find_one", return_value=None)
async def test_on_boarding_user_current_step_us_when_current_user_is_none_the_raise_unique_id_doesnt_exists_error(
        mock_find_one,
        mock_user_file_exists,
):
    with pytest.raises(UserUniqueIdDoesNotExists):
        await UserOnBoardingStepsService.onboarding_user_current_step_br(
            unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491"
        )


@pytest.mark.asyncio
@patch.object(
    UserOnBoardingStepsService,
    "onboarding_user_current_step_us",
    return_value=onboarding_user_current_step_us_stub
)
async def test_onboarding_us_step_validator_when_sending_right_params_then_return_expected_which_is_none(
        mock_onboarding_user_current_step_us
):
    response = await UserOnBoardingStepsService.onboarding_us_step_validator(
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
        onboard_step=['w8_confirmation_step', 'finished']
    )
    assert response is None


@pytest.mark.asyncio
@patch.object(
    UserOnBoardingStepsService,
    "onboarding_user_current_step_us",
    return_value=onboarding_user_invalid_current_step_us_stub
)
async def test_onboarding_us_step_validator_when_sending_right_params_then_raise_error(
        mock_onboarding_user_current_step_us
):
    with pytest.raises(InvalidOnboardingStep):
        await UserOnBoardingStepsService.onboarding_us_step_validator(
            unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
            onboard_step=['w8_confirmation_step', 'finished']
        )


@pytest.mark.asyncio
@patch.object(
    UserOnBoardingStepsService,
    "onboarding_user_current_step_br",
    return_value=onboarding_user_current_step_us_stub
)
async def test_onboarding_br_step_validator_when_sending_right_params_then_return_expected_which_is_none(
        mock_onboarding_user_current_step_br
):
    response = await UserOnBoardingStepsService.onboarding_br_step_validator(
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
        onboard_step=['w8_confirmation_step', 'finished']
    )
    assert response is None


@pytest.mark.asyncio
@patch.object(
    UserOnBoardingStepsService,
    "onboarding_user_current_step_br",
    return_value=onboarding_user_invalid_current_step_us_stub
)
async def test_onboarding_br_step_validator_when_sending_right_params_then_raise_error(
        mock_onboarding_user_current_step_us
):
    with pytest.raises(InvalidOnboardingStep):
        await UserOnBoardingStepsService.onboarding_br_step_validator(
            unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491",
            onboard_step=['w8_confirmation_step', 'finished']
        )
