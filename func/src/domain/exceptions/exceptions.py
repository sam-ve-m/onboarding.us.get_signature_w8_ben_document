class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique_id," \
          " jwt not decoded successfully"


class UserUniqueIdDoesNotExists(Exception):
    msg = "Jormungandr-Onboarding::get_registration_data::Not exists an user with this unique_id"


class InternalServerError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class BadRequestError(Exception):
    pass
