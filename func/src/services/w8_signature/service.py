# STANDARD IMPORTS
import asyncio
from fastapi import status

# THIRD PARTY IMPORTS
from persephone_client import Persephone
from func.src.domain.persephone_queue.persephone_queue import PersephoneQueue

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import InternalServerError
from func.src.infrastructure.env_config import config
from func.src.repositories.file.repository import FileRepository
from func.src.repositories.user.repository import UserRepository
from func.src.services.persephone.model import get_w8_form_confirmation_schema_template_with_data
from func.src.services.onboarding_steps.service import UserOnBoardingStepsService


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
            cls, payload: dict) -> dict:

        unique_id, w8_form_confirmation = cls.__extract_unique_id(payload=payload)

        br_step_validator = await UserOnBoardingStepsService.onboarding_br_step_validator(
            unique_id=unique_id, onboard_step=["finished"]
        )
        us_step_validator = await UserOnBoardingStepsService.onboarding_us_step_validator(
            unique_id=unique_id, onboard_step=["w8_confirmation_step", "finished"]
        )
        await asyncio.gather(br_step_validator, us_step_validator)

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserOnBoardingStepsService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_W8_CONFIRMATION_US.value,
            message=get_w8_form_confirmation_schema_template_with_data(
                w8_form_confirmation=w8_form_confirmation,
                unique_id=unique_id
            ),
            schema_name="user_w8_form_confirmation_us_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        was_updated = await cls.user_repository.update_one(
            old={"unique_id": unique_id},
            new={
                "external_exchange_requirements.us.w8_confirmation": w8_form_confirmation,
            },
        )
        if not was_updated:
            raise InternalServerError("common.unable_to_process")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }
