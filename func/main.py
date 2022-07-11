# STANDARD IMPORTS
from http import HTTPStatus
from flask import Request, request, Response, Flask

from etria_logger import Gladsheim
from func.src.domain.enums.status_code.enum import InternalCode
from func.src.domain.exceptions.exceptions import ErrorOnDecodeJwt
from func.src.domain.response.model import ResponseModel
from func.src.domain.validators.validator import W8FormConfirmation
from func.src.services.jwt_service.service import JWTService
from func.src.services.w8_signature.service import W8DocumentService

app = Flask(__name__)


@app.route('/update_w8_ben_signature')
async def update_w8_ben_signature(
        w8_form_confirmation: W8FormConfirmation,
        request_body: Request = request,
):
    jwt_data = request_body.headers.get("x-thebes-answer")
    payload = await JWTService.get_thebes_answer_from_request(jwt_data=jwt_data)
    payload = {"x-thebes-answer": payload}
    payload.update(w8_form_confirmation.dict())
    try:
        response = await W8DocumentService.update_w8_form_confirmation(payload=payload)
        return response

    except ErrorOnDecodeJwt as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Invalid JWT"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ValueError:
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
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
