# STANDARD IMPORTS
import asyncio

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import W8DocumentWasNotUpdated
from src.domain.models.jwt.response import Jwt
from src.domain.models.w8_signature.base.model import W8FormConfirmation
from src.repositories.user.repository import UserRepository
from src.services.iara_client.service import SendToIara
from src.services.persephone.service import SendToPersephone
from src.transport.onboarding_steps_br.transport import ValidateOnboardingStepsBr
from src.transport.onboarding_steps_us.transport import ValidateOnboardingStepsUS


class W8DocumentService:

    @classmethod
    async def update_w8_form_confirmation(
            cls,
            w8_confirmation_request: W8FormConfirmation,
            jwt_data: Jwt,

    ):
        br_step_validator = ValidateOnboardingStepsBr.validate_onboarding_steps_br(
            jwt_data=jwt_data
        )
        us_step_validator = ValidateOnboardingStepsUS.validate_onboarding_steps_us(
            jwt_data=jwt_data
        )
        await asyncio.gather(br_step_validator, us_step_validator)

        await SendToPersephone.register_w8_confirmation_log(
            jwt_data=jwt_data,
            w8_confirmation_request=w8_confirmation_request
        )

        was_updated = await UserRepository.update_user_and_us_w8_confirmation(
            w8_confirmation_request=w8_confirmation_request.w8_form_confirmation,
            unique_id=jwt_data.get_unique_id_from_jwt_payload()
        )

        if not was_updated:
            raise W8DocumentWasNotUpdated(
                "common.unable_to_process::W8DocumentService::update_w8_form_confirmation::was_updated::false"
            )

        await SendToIara.register_user_w8_signature_log_on_persephone(
            jwt_data=jwt_data
        )

        return bool(was_updated)
