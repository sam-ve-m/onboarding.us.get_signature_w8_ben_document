# STANDARD IMPORTS
import pytest

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import InvalidOnboardingStep
from func.src.domain.validators.onboarding_steps_us.validator import (
    OnboardingStepsUsValidator,
)


step_response_stub = {"result": {"current_step": "w8_confirmation"}}

step_not_finished_stub = {"result": {"current_step": "nothing yet"}}


@pytest.mark.asyncio
async def test_when_sending_right_params_to_onboarding_us_step_validator_then_return_the_expected():
    response = await OnboardingStepsUsValidator.onboarding_us_step_validator(
        step_response=step_response_stub
    )
    assert response is True


@pytest.mark.asyncio
async def test_when_not_sending_right_params_then_raise_error():
    with pytest.raises(AttributeError):
        await OnboardingStepsUsValidator.onboarding_us_step_validator(
            step_response=None
        )


@pytest.mark.asyncio
async def test_when_sending_right_params_but_step_is_not_finished_then_raise_invalid_us_onboarding_step():
    with pytest.raises(Exception):
        await OnboardingStepsUsValidator.onboarding_us_step_validator(
            step_response=step_not_finished_stub
        )
