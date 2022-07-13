# STANDARD IMPORTS
from http import HTTPStatus
from aioflask import Flask, request, Response, Request

# THIRD PARTY IMPORTS
from etria_logger import Gladsheim

# PROJECT IMPORTS
from src.domain.enums.status_code.enum import InternalCode
from src.domain.exceptions.exceptions import ErrorOnDecodeJwt, WasNotSentToPersephone, InvalidParams
from src.domain.response.model import ResponseModel
from src.domain.validators.validator import W8FormConfirmation
from src.services.jwt_service.service import JWTService
from src.services.w8_signature.service import W8DocumentService

app = Flask(__name__)


@app.route('/update_w8_ben_signature')
async def update_w8_ben_signature(
        request_body: Request = request,
) -> Response:
    raw_params = request.json
    w8_confirmation_param = W8FormConfirmation(**raw_params).dict()
    jwt_data = request_body.headers.get("x-thebes-answer")
    thebes_answer = await JWTService.decode_jwt_from_request(jwt_data=jwt_data)
    payload = {"x-thebes-answer": thebes_answer}
    payload.update(w8_confirmation_param)

    try:
        service_response = await W8DocumentService.update_w8_form_confirmation(payload=payload)
        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="The W8 Form Was Updated Successfully",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidParams as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid Params were sent"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Invalid JWT"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except WasNotSentToPersephone as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.WAS_NOT_SENT_TO_PERSEPHONE,
            message="update_w8_form_confirmation::sent_to_persephone:false"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except TypeError as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.NOT_DATE_TIME,
            message="months_past::submission_date is not a datetime"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response


if __name__ == "__main__":
    app.run(debug=True)
