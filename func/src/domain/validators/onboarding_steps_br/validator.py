# PROJECT IMPORTS
from src.domain.exceptions.exceptions import InvalidOnboardingStep


class OnboardingStepsBrValidator:

    expected_step_br = "finished"

    @classmethod
    async def onboarding_br_step_validator(cls, step_response: dict) -> bool:
        response = step_response.get("result", {}).get("current_step")

        step_is_valid = response in cls.expected_step_br

        if not step_is_valid:
            raise InvalidOnboardingStep()

        return step_is_valid
