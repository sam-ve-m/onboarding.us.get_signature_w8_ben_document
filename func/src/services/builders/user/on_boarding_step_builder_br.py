from func.src.domain.enums.caf.enum import CAFStatus


class OnboardingStepBuilderBR:
    def __init__(self):
        self.__onboarding_steps: dict = {
            "current_onboarding_step": "suitability_step",
            "suitability_step": False,
            "user_identifier_data_step": False,
            "user_selfie_step": False,
            "user_complementary_step": False,
            "user_document_validator": False,
            "user_data_validation": False,
            "user_electronic_signature": False,
            "finished": False,
        }
        self.__steps: list = [
            "suitability_step",
            "user_identifier_data_step",
            "user_selfie_step",
            "user_complementary_step",
            "user_document_validator",
            "user_data_validation",
            "user_electronic_signature",
        ]
        self.bureau_status = None

    def user_suitability_step(self, current_user):
        user_suitability_profile = current_user.get("suitability")
        terms = current_user.get("terms")
        has_signed_refusal_term = terms.get("term_refusal")
        if (
            user_suitability_profile is not None or has_signed_refusal_term is not None
        ) and self.__onboarding_steps["current_onboarding_step"] == "suitability_step":
            self.__onboarding_steps["suitability_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_identifier_data_step"
        return self

    def user_identifier_step(self, current_user: dict):
        user_cpf = current_user.get("identifier_document", {}).get("cpf")
        user_cel_phone = current_user.get("phone")
        if (
            user_cpf is not None
            and user_cel_phone is not None
            and self.__onboarding_steps["current_onboarding_step"]
            == "user_identifier_data_step"
        ):
            self.__onboarding_steps["user_identifier_data_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "user_selfie_step"

        return self

    def user_selfie_step(self, user_file_exists: bool):
        if (
            user_file_exists
            and self.__onboarding_steps["current_onboarding_step"] == "user_selfie_step"
        ):
            self.__onboarding_steps["user_selfie_step"] = user_file_exists
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_complementary_step"

        return self

    def user_complementary_step(self, current_user):
        marital = current_user.get("marital")

        if (
            marital is not None
            and self.__onboarding_steps["current_onboarding_step"]
            == "user_complementary_step"
        ):
            self.__onboarding_steps["user_complementary_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_document_validator"

        return self

    def user_document_validator_step(self, current_user, document_exists: bool):
        bureau_status = current_user.get("bureau_status")

        if bureau_status is not None:
            self.bureau_status = bureau_status

        if self.__onboarding_steps[
            "current_onboarding_step"
        ] == "user_document_validator" and (
            (bureau_status and bureau_status != CAFStatus.DOCUMENT.value)
            or document_exists
        ):
            self.__onboarding_steps["user_document_validator"] = True
            self.__onboarding_steps["current_onboarding_step"] = "user_data_validation"

        return self

    def user_data_validation_step(self, current_user):
        has_validate_data = current_user.get("is_bureau_data_validated")

        if (
            has_validate_data
            and self.__onboarding_steps["current_onboarding_step"]
            == "user_data_validation"
        ):
            self.__onboarding_steps["user_data_validation"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_electronic_signature"

        return self

    def user_electronic_signature_step(self, current_user):
        has_electronic_signature = current_user.get("electronic_signature")
        if (
            has_electronic_signature is not None
            and self.__onboarding_steps["current_onboarding_step"]
            == "user_electronic_signature"
        ):
            self.__onboarding_steps["user_electronic_signature"] = True
        return self

    def is_finished(self):
        if all([self.__onboarding_steps[step] for step in self.__steps]):
            self.__onboarding_steps["current_onboarding_step"] = "finished"
            self.__onboarding_steps["finished"] = True
        elif self.bureau_status == CAFStatus.REFUSED.value:
            self.__onboarding_steps["finished"] = True
            self.__onboarding_steps["current_onboarding_step"] = self.bureau_status

    async def build(self) -> dict:
        self.is_finished()
        onboarding_steps = self.__onboarding_steps
        return onboarding_steps
