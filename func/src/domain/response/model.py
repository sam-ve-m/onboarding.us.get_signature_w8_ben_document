# STANDARD IMPORTS
from json import dumps
from flask import Response

# PROJECT IMPORTS
from func.src.domain.enums.status_code.enum import InternalCode


class ResponseModel:
    def __init__(
            self,
            success: bool,
            code: InternalCode,
            message: str = None,
            result: any = None):

        self.success = success
        self.code = code
        self.message = message
        self.result = result
        self.response = self.to_dumps()

    def to_dumps(self) -> str:
        response_model = dumps(
            {
                "result": self.result,
                "message": self.message,
                "success": self.success,
                "code": self.code,
            }
        )

        self.response = response_model
        return response_model

    @staticmethod
    def build_response(
            success: bool, code: InternalCode, message: str = None, result: any = None
    ):
        response_model = dumps(
            {
                "result": result,
                "message": message,
                "success": success,
                "code": code.value,
            }
        )
        return response_model

    @staticmethod
    def build_http_response(
            status: int, response_model: str = None, mimetype: str = "application/json"
    ) -> Response:
        response = Response(
            response_model,
            mimetype=mimetype,
            status=status,
        )
        return response
