class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique_id," \
          " jwt not decoded successfully"


class InvalidOnboardingStep(Exception):
    pass


class UserUniqueIdDoesNotExists(Exception):
    pass


class W8DocumentWasNotUpdated(Exception):
    pass


class WasNotSentToPersephone(Exception):
    msg = "common.process_issue::W8DocumentService::update_w8_form_confirmation::sent_to_persephone:false"


class InternalServerError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class BadRequestError(Exception):
    pass
