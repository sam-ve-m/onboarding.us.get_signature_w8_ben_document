from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Response, Request
from pydantic import ValidationError

from src.domain.enums.status_code.enum import InternalCode
from src.domain.exceptions.exceptions import (
    ErrorOnDecodeJwt,
    NotSentToPersephone,
    TransportOnboardingError,
    InvalidOnboardingStep,
    UserUniqueIdDoesNotExists,
)
from src.domain.models.jwt.response import Jwt
from src.domain.models.response.model import ResponseModel
from src.domain.models.w8_signature.base.model import W8FormConfirmation
from src.services.w8_signature.service import W8DocumentService


async def update_w8_ben(
    request_body: Request = request,
) -> Response:
    thebes_answer = request_body.headers.get("x-thebes-answer")

    try:
        jwt_data = Jwt(jwt=thebes_answer)
        await jwt_data()
        w8_confirmation_request = W8FormConfirmation(**request_body.json)

        service_response = await W8DocumentService.update_w8_form_confirmation(
            jwt_data=jwt_data, w8_confirmation_request=w8_confirmation_request
        )
        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="The W8 Form Was Updated Successfully",
            result=service_response,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidOnboardingStep as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_ONBOARDING_STEPS,
            message="User in invalid onboarding step",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message="Invalid JWT"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except NotSentToPersephone as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.WAS_NOT_SENT_TO_PERSEPHONE,
            message="update_w8_form_confirmation::sent_to_persephone:false",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except TransportOnboardingError as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.TRANSPORT_ON_BOARDING_ERROR,
            message="update_w8_form_confirmation::error fetching data from transport layer",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except UserUniqueIdDoesNotExists as error:
        Gladsheim.error(error=error, message=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.USER_WAS_NOT_FOUND,
            message="UserRepository.update_user_and_us_w8_confirmation::unique id was not found",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValidationError as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid request"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except TypeError as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.NOT_DATE_TIME,
            message="months_past::submission_date is not a datetime",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
