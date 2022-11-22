class ErrorOnDecodeJwt(Exception):
    msg = (
        "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique_id,"
        " jwt not decoded successfully"
    )


class InvalidOnboardingStep(Exception):
    msg = (
        "common.process.issue::onboarding_step_validator::user.invalid_on_boarding_step"
    )


class TransportOnboardingError(Exception):
    msg = "Jormungandr-Onboarding::ValidateOnboardingSteps::error on fetching data from fission steps"


class UserUniqueIdDoesNotExists(Exception):
    pass


class W8DocumentWasNotUpdated(Exception):
    pass


class HttpErrorGettingOnboardingSteps(Exception):
    msg = (
        "common_process_issue::ValidateOnboardingStepsUS::validate_onboarding_steps_us"
    )


class NotSentToPersephone(Exception):
    msg = "common.process_issue::W8DocumentService::update_w8_form_confirmation::sent_to_persephone:false"


class DeviceInfoRequestFailed(Exception):
    msg = "Error trying to get device info"


class DeviceInfoNotSupplied(Exception):
    msg = "Device info not supplied"
