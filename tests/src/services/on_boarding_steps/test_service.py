# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import UserUniqueIdDoesNotExists
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import UserOnBoardingStepsService

# STUBS
from tests.src.services.on_boarding_steps.service_stub import find_one_stub_steps, builder_stub_on_boarding_steps, \
    builder_stub_us_onbording


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
