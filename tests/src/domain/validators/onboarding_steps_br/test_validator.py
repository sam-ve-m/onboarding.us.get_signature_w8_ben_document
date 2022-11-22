import pytest

from func.src.domain.validators.onboarding_steps_br.validator import (
    OnboardingStepsBrValidator,
)
from tests.src.domain.validators.onboarding_steps_br.file_stub import (
    step_response_stub,
    step_not_finished_stub,
)


@pytest.mark.asyncio
async def test_when_sending_right_params_to_onboarding_br_step_validator_then_return_the_expected():
    response = await OnboardingStepsBrValidator.onboarding_br_step_validator(
        step_response=step_response_stub
    )
    assert response is True


@pytest.mark.asyncio
async def test_when_not_sending_right_params_then_raise_error():
    with pytest.raises(AttributeError):
        await OnboardingStepsBrValidator.onboarding_br_step_validator(
            step_response=None
        )


@pytest.mark.asyncio
async def test_when_sending_right_params_but_step_is_not_finished_then_raise_invalid_onboarding_br_step():
    with pytest.raises(Exception):
        await OnboardingStepsBrValidator.onboarding_br_step_validator(
            step_response=step_not_finished_stub
        )
