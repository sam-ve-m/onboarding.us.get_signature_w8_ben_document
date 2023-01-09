from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Response, Request
from pydantic import ValidationError

from func.src.domain.enums.status_code.enum import InternalCode
from func.src.domain.exceptions.exceptions import (
    ErrorOnDecodeJwt,
    NotSentToPersephone,
    TransportOnboardingError,
    InvalidOnboardingStep,
    UserUniqueIdDoesNotExists,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from func.src.domain.models.jwt.response import Jwt
from func.src.domain.models.response.model import ResponseModel
from func.src.domain.models.w8_signature.base.model import W8FormConfirmation
from func.src.services.w8_signature.service import W8DocumentService
from func.src.transport.device_info.transport import DeviceSecurity


async def update_w8_ben(
    request: Request = request,
) -> Response:
    try:
        x_thebes_answer = request.headers.get("x-thebes-answer")
        x_device_info = request.headers.get("x-device-info")
        request_body = request.json

        jwt_data = Jwt(jwt=x_thebes_answer)
        await jwt_data()
        device_info = await DeviceSecurity.get_device_info(x_device_info)
        w8_confirmation_request = W8FormConfirmation(**request_body)

        service_response = await W8DocumentService.update_w8_form_confirmation(
            jwt_data=jwt_data,
            w8_confirmation_request=w8_confirmation_request,
            device_info=device_info,
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
            code=InternalCode.INVALID_PARAMS,
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
        Gladsheim.error(error=error, message="unique id does not exist")
        response = ResponseModel(
            success=False,
            code=InternalCode.USER_WAS_NOT_FOUND,
            message="UserRepository.update_user_and_us_w8_confirmation::unique id was not found",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValidationError as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid request"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except DeviceInfoRequestFailed as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Error trying to get device info",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Device info not supplied",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except TypeError as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.NOT_DATE_TIME,
            message="months_past::submission_date is not a datetime",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
