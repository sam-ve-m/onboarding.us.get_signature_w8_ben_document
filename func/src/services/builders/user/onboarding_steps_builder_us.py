# PROJECT IMPORTS
from src.repositories.file.enum.term_file import TermsFileType


class OnboardingStepBuilderUS:

    def __init__(self):
        self.__onboarding_steps: dict = {
            "current_onboarding_step": "terms_step",
            "terms_step": False,
            "user_document_validator_step": False,
            "is_politically_exposed_step": False,
            "is_exchange_member_step": False,
            "is_company_director_step": False,
            "external_fiscal_tax_confirmation_step": False,
            "employ_step": False,
            "time_experience_step": False,
            "w8_confirmation_step": False,
            "finished": False,
        }
        self.__steps: list = [
            "terms_step",
            "user_document_validator_step",
            "is_politically_exposed_step",
            "is_exchange_member_step",
            "is_company_director_step",
            "external_fiscal_tax_confirmation_step",
            "employ_step",
            "time_experience_step",
            "w8_confirmation_step",
        ]
        self.bureau_status = None

    def terms_step(self, current_user: dict):
        user_terms = current_user.get("terms")
        user_signed_terms = set(
            [
                term_name if metadata else None
                for term_name, metadata in user_terms.items()
            ]
        )
        terms_that_needs_be_signed = {
            TermsFileType.TERM_OPEN_ACCOUNT_DW.value,
            TermsFileType.TERM_APPLICATION_DW.value,
            TermsFileType.TERM_PRIVACY_POLICY_AND_DATA_SHARING_POLICY_DW.value,
            TermsFileType.TERM_DISCLOSURES_AND_DISCLAIMERS.value,
            TermsFileType.TERM_MONEY_CORP.value,
            TermsFileType.TERM_GRINGO_WORLD.value,
            TermsFileType.TERM_GRINGO_WORLD_GENERAL_ADVICES.value,
        }
        all_terms_is_signed = not (terms_that_needs_be_signed - user_signed_terms)
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"] == "terms_step"
        )
        if all_terms_is_signed and is_valid_onbaording_step:
            self.__onboarding_steps["terms_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "user_document_validator_step"
        return self

    def user_document_validator_step(self, document_exists: bool):
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"]
            == "user_document_validator_step"
        )
        if is_valid_onbaording_step and document_exists:
            self.__onboarding_steps["user_document_validator_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "is_politically_exposed_step"

        return self

    def is_politically_exposed_step(self, current_user: dict):
        politically_exposed = (
            current_user.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_politically_exposed")
        )
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"]
            == "is_politically_exposed_step"
        )
        if is_valid_onbaording_step and politically_exposed is not None:
            self.__onboarding_steps["is_politically_exposed_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "is_exchange_member_step"
        return self

    def is_exchange_member_step(self, current_user: dict):
        is_exchange_member = (
            current_user.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_exchange_member")
        )
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"]
            == "is_exchange_member_step"
        )
        if is_valid_onbaording_step and is_exchange_member is not None:
            self.__onboarding_steps["is_exchange_member_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "is_company_director_step"
        return self

    def is_company_director_step(self, current_user: dict):
        is_exchange_member = (
            current_user.get("external_exchange_requirements", {})
            .get("us", {})
            .get("is_company_director")
        )
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"]
            == "is_company_director_step"
        )
        if is_valid_onbaording_step and is_exchange_member is not None:
            self.__onboarding_steps["is_company_director_step"] = True
            self.__onboarding_steps[
                "current_onboarding_step"
            ] = "external_fiscal_tax_confirmation_step"
        return self

    def external_fiscal_tax_confirmation_step(self, current_user: dict):
        is_exchange_member = (
            current_user.get("external_exchange_requirements", {})
            .get("us", {})
            .get("external_fiscal_tax_confirmation")
        )
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"]
            == "external_fiscal_tax_confirmation_step"
        )
        if is_valid_onbaording_step and is_exchange_member:
            self.__onboarding_steps["external_fiscal_tax_confirmation_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "employ_step"
        return self

    def employ_step(self, current_user: dict):
        user_employ_status = (
            current_user.get("external_exchange_requirements", {})
            .get("us", {})
            .get("user_employ_status")
        )
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"] == "employ_step"
        )
        if is_valid_onbaording_step and user_employ_status:
            self.__onboarding_steps["employ_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "time_experience_step"
        return self

    def time_experience_step(self, current_user: dict):
        is_exchange_member = (
            current_user.get("external_exchange_requirements", {})
            .get("us", {})
            .get("time_experience")
        )
        user_was_created_on_dw = (
            current_user["portfolios"]["default"].get("us", {}).get("dw_id")
        )
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"] == "time_experience_step"
        )
        if is_valid_onbaording_step and user_was_created_on_dw and is_exchange_member:
            self.__onboarding_steps["time_experience_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "w8_confirmation_step"
        return self

    def w8_confirmation_step(self, current_user: dict):
        is_exchange_member = (
            current_user.get("external_exchange_requirements", {})
            .get("us", {})
            .get("w8_confirmation")
        )
        is_valid_onbaording_step = (
            self.__onboarding_steps["current_onboarding_step"] == "w8_confirmation_step"
        )
        if is_valid_onbaording_step and is_exchange_member:
            self.__onboarding_steps["w8_confirmation_step"] = True
            self.__onboarding_steps["current_onboarding_step"] = "finished"
        return self

    def is_finished(self):
        if all([self.__onboarding_steps[step] for step in self.__steps]):
            self.__onboarding_steps["current_onboarding_step"] = "finished"
            self.__onboarding_steps["finished"] = True

    async def build(self) -> dict:
        self.is_finished()
        onboarding_steps = self.__onboarding_steps
        return onboarding_steps
