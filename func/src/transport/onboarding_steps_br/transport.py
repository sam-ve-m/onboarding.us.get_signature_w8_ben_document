# STANDARD IMPORTS
import aiohttp

# THIRD PART IMPORTS
from decouple import config

from func.src.domain.exceptions.exceptions import TransportOnboardingError
from etria_logger import Gladsheim

# PROJECT IMPORTS
from func.src.domain.models.jwt.response import Jwt
from func.src.domain.validators.onboarding_steps_br.validator import (
    OnboardingStepsBrValidator,
)


class ValidateOnboardingStepsBr:

    steps_br_url = config("BR_BASE_URL")

    @classmethod
    async def validate_onboarding_steps_br(cls, jwt_data: Jwt):
        headers = {"x-thebes-answer": "{}".format(jwt_data.get_jwt())}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(cls.steps_br_url, headers=headers) as response:
                    step_response = await response.json()
        except Exception as error:
            Gladsheim.error(error=error)
            raise TransportOnboardingError()

        step_is_valid = await OnboardingStepsBrValidator.onboarding_br_step_validator(
            step_response=step_response
        )
        return step_is_valid
