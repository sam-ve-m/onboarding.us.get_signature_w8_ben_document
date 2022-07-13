# STANDARD IMPORTS
import asyncio
from typing import List
from fastapi import status

# PROJECT IMPORTS
from persephone_client import Persephone

from src.domain.exceptions.exceptions import BadRequestError, UserUniqueIdDoesNotExists, InvalidOnboardingStep
from src.infrastructure.env_config import config
from src.repositories.file.enum.user_file import UserFileType
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.builders.user.on_boarding_step_builder_br import OnboardingStepBuilderBR
from src.services.builders.user.onboarding_steps_builder_us import OnboardingStepBuilderUS


class UserOnBoardingStepsService:
    persephone_client = Persephone

    # TODO - once the on boarding steps fissions were implemented, replace the services for a layer
    @classmethod
    async def onboarding_user_current_step_br(
            cls, unique_id: str
    ) -> dict:
        onboarding_step_builder = OnboardingStepBuilderBR()

        user_file_exists = await FileRepository.user_file_exists(
            file_type=UserFileType.SELFIE,
            unique_id=unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        user_document_front_exists = FileRepository.user_file_exists(
            file_type=UserFileType.DOCUMENT_FRONT,
            unique_id=unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        user_document_back_exists = FileRepository.user_file_exists(
            file_type=UserFileType.DOCUMENT_BACK,
            unique_id=unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        user_document_exists = all(
            await asyncio.gather(user_document_front_exists, user_document_back_exists)
        )

        current_user = await UserRepository.find_one({"unique_id": unique_id})
        if current_user is None:
            raise UserUniqueIdDoesNotExists(
                "common.process.issue::onboarding_user_current_step_br::user_repository.find_one::user_does_exists")

        onboarding_steps = await (
            onboarding_step_builder.user_suitability_step(current_user=current_user)
                .user_identifier_step(current_user=current_user)
                .user_selfie_step(user_file_exists=user_file_exists)
                .user_complementary_step(current_user=current_user)
                .user_document_validator_step(
                current_user=current_user, document_exists=user_document_exists
            )
                .user_data_validation_step(current_user=current_user)
                .user_electronic_signature_step(current_user=current_user)
                .build()
        )

        return onboarding_steps

    @classmethod
    async def onboarding_user_current_step_us(
            cls,
            unique_id: str
    ) -> dict:
        onboarding_step_builder = OnboardingStepBuilderUS()

        current_user = await UserRepository.find_one({"unique_id": unique_id})

        if current_user is None:
            raise UserUniqueIdDoesNotExists(
                "common.process.issue::onboarding_user_current_step_br::user_repository.find_one::user_does_exists")

        user_document_front_exists = FileRepository.user_file_exists(
            file_type=UserFileType.DOCUMENT_FRONT,
            unique_id=unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        user_document_back_exists = FileRepository.user_file_exists(
            file_type=UserFileType.DOCUMENT_BACK,
            unique_id=unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        user_document_exists = all(
            await asyncio.gather(user_document_front_exists, user_document_back_exists)
        )

        onboarding_steps = await (
            onboarding_step_builder.terms_step(current_user=current_user)
                .user_document_validator_step(document_exists=user_document_exists)
                .is_politically_exposed_step(current_user=current_user)
                .is_exchange_member_step(current_user=current_user)
                .is_company_director_step(current_user=current_user)
                .external_fiscal_tax_confirmation_step(current_user=current_user)
                .employ_step(current_user=current_user)
                .time_experience_step(current_user=current_user)
                .w8_confirmation_step(current_user=current_user)
                .build()
        )

        return onboarding_steps

    @classmethod
    async def onboarding_us_step_validator(
            cls,
            unique_id: str,
            onboard_step: List[str]):
        onboarding_steps = await cls.onboarding_user_current_step_us(unique_id=unique_id)
        current_onboarding_step = onboarding_steps.get(
            "current_onboarding_step"
        )
        if current_onboarding_step not in onboard_step:
            raise InvalidOnboardingStep(
                "common.process.issue::onboarding_us_step_validator::user.invalid_on_boarding_step"
            )

    @staticmethod
    async def onboarding_br_step_validator(unique_id: str, onboard_step: List[str]):
        onboarding_steps = await UserOnBoardingStepsService.onboarding_user_current_step_br(unique_id)
        current_onboarding_step = onboarding_steps.get(
            "current_onboarding_step"
        )
        if current_onboarding_step not in onboard_step:
            raise InvalidOnboardingStep(
                "common.process.issue::onboarding_br_step_validator::user.invalid_on_boarding_step"
            )
