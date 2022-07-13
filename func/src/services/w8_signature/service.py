# STANDARD IMPORTS
import asyncio
from persephone_client import Persephone

# THIRD PARTY IMPORTS
from src.domain.persephone.model import GetW8ConfirmationTemplate
from src.domain.persephone_queue.persephone_queue import PersephoneQueue

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import W8DocumentWasNotUpdated, WasNotSentToPersephone
from src.infrastructure.env_config import config
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import UserOnBoardingStepsService


class W8DocumentService:
    persephone_client = Persephone
    user_repository = UserRepository
    file_repository = FileRepository

    @classmethod
    def __extract_unique_id(cls, payload: dict):
        unique_id = payload.get("x-thebes-answer").get("user").get("unique_id")
        w8_form_confirmation = payload.get("w8_confirmation")
        return unique_id, w8_form_confirmation

    @classmethod
    async def update_w8_form_confirmation(
            cls, payload: dict):

        unique_id, w8_form_confirmation = cls.__extract_unique_id(payload=payload)

        br_step_validator = UserOnBoardingStepsService.onboarding_br_step_validator(
            unique_id=unique_id, onboard_step=["finished"]
        )
        us_step_validator = UserOnBoardingStepsService.onboarding_us_step_validator(
            unique_id=unique_id, onboard_step=["w8_confirmation_step", "finished"]
        )
        await asyncio.gather(br_step_validator, us_step_validator)

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserOnBoardingStepsService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_W8_CONFIRMATION_US.value,
            message=GetW8ConfirmationTemplate.get_w8_form_confirmation_schema_template_with_data(
                w8_form_confirmation=w8_form_confirmation,
                unique_id=unique_id
            ),
            schema_name="user_w8_form_confirmation_us_schema",
        )

        if sent_to_persephone is False:
            raise WasNotSentToPersephone(
                "common.process_issue::W8DocumentService::update_w8_form_confirmation::sent_to_persephone:false"
            )

        was_updated = await cls.user_repository.update_one(
            old={"unique_id": unique_id},
            new={"external_exchange_requirements.us.w8_confirmation": w8_form_confirmation,},
        )

        if not was_updated:
            raise W8DocumentWasNotUpdated(
                "common.unable_to_process::W8DocumentService::update_w8_form_confirmation::was_updated::false"
            )

        return bool(was_updated)
