from persephone_client import Persephone
from func.src.services.builders.user.on_boarding_step_builder_br import OnboardingStepBuilderBR


class UserService:

    persephone_client = Persephone
    user_repository = UserRepository
    file_repository = FileRepository

    @staticmethod
    async def onboarding_user_current_step_br(
        payload: dict        
    ) -> dict:
        onboarding_step_builder = OnboardingStepBuilderBR()
        x_thebes_answer = payload.get("x-thebes-answer")
        user_unique_id = x_thebes_answer["user"]["unique_id"]

        user_file_exists = await file_repository.user_file_exists(
            file_type=UserFileType.SELFIE,
            unique_id=user_unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        user_document_front_exists = file_repository.user_file_exists(
            file_type=UserFileType.DOCUMENT_FRONT,
            unique_id=user_unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        user_document_back_exists = file_repository.user_file_exists(
            file_type=UserFileType.DOCUMENT_BACK,
            unique_id=user_unique_id,
            bucket_name=config("AWS_BUCKET_USERS_FILES"),
        )
        user_document_exists = all(
            await asyncio.gather(user_document_front_exists, user_document_back_exists)
        )

        current_user = await user_repository.find_one({"unique_id": user_unique_id})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")

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

        return {"status_code": status.HTTP_200_OK, "payload": onboarding_steps}

    @staticmethod
    async def onboarding_us_step_validator(payload: dict, onboard_step: List[str]):
        onboarding_steps = await UserService.onboarding_user_current_step_us(payload)
        payload_from_onboarding_steps = onboarding_steps.get("payload")
        current_onboarding_step = payload_from_onboarding_steps.get(
            "current_onboarding_step"
        )
        if current_onboarding_step not in onboard_step:
            raise BadRequestError("user.invalid_on_boarding_step")


    @staticmethod
    async def onboarding_br_step_validator(payload: dict, onboard_step: List[str]):
        onboarding_steps = await UserService.onboarding_user_current_step_br(payload)
        payload_from_onboarding_steps = onboarding_steps.get("payload")
        current_onboarding_step = payload_from_onboarding_steps.get(
            "current_onboarding_step"
        )
        if current_onboarding_step not in onboard_step:
            raise BadRequestError("user.invalid_on_boarding_step")

    @staticmethod
    async def update_w8_form_confirmation(
            payload: dict, user_repository=UserRepository
    ) -> dict:
        thebes_answer = payload["x-thebes-answer"]
        thebes_answer_user = thebes_answer["user"]
        user_w8_form_confirmation = payload["w8_confirmation"]
        br_step_validator = UserService.onboarding_br_step_validator(
            payload=payload, onboard_step=["finishefinishedd"]
        )
        us_step_validator = UserService.onboarding_us_step_validator(
            payload=payload, onboard_step=["w8_confirmation_step", "finished"]
        )
        await asyncio.gather(br_step_validator, us_step_validator)

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_W8_CONFIRMATION_US.value,
            message=get_w8_form_confirmation_schema_template_with_data(
                w8_form_confirmation=user_w8_form_confirmation,
                unique_id=thebes_answer["user"]["ununique_idique_id"],
            ), )
        schema_name = "user_w8_form_confirmation_us_schema",

        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        unique_id = thebes_answer_user["unique_id"]
        was_updated = await user_repository.update_one(
            old={"unique_id": unique_id}, old={"unique_id": unique_id},

            new={
                "external_exchange_requirements.us.w8_confirmation": user_w8_form_confirmation,
            },
        )
        if not was_updated:
            raise InternalServerError("common.unable_to_process")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }