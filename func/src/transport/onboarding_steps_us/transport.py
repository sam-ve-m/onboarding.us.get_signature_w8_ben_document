# STANDARD IMPORTS
from http import HTTPStatus
import requests
import aiohttp

# THIRD PART IMPORTS
from decouple import config
from src.domain.models.response.model import ResponseModel
from etria_logger import Gladsheim

# PROJECT IMPORTS
from src.domain.enums.status_code.enum import InternalCode
from src.domain.models.jwt.response import Jwt
from src.domain.validators.onboarding_steps_us.validator import OnboardingStepsUsValidator


class ValidateOnboardingStepsUS:
    steps_us_url = config("US_BASE_URL")

    @classmethod
    async def validate_onboarding_steps_us(cls, jwt_data: Jwt):
        headers = {'x-thebes-answer': "{}".format(jwt_data.get_jwt())}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(cls.steps_us_url, headers=headers) as response:
                    step_response = await response.json()

                    step_is_valid = await OnboardingStepsUsValidator.onboarding_us_step_validator(
                        step_response=step_response
                    )

                    return step_is_valid

        except requests.exceptions.ConnectionError as error:
            Gladsheim.error(error=error)
            response = ResponseModel(
                result=False,
                success=False,
                code=InternalCode.HTTP_CONNECTION_POLL,
                message="Error On HTTP Request"
            ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return response
