import asyncio
from persephone_client import Persephone
from func.src.domain.exceptions.exceptions import InternalServerError


async def put_w8_form_confirmation(
    w8_form_confirmation: W8FormConfirmation,
    request: Request,
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {"x-thebes-answer": jwt_data}
    payload.update(w8_form_confirmation.dict())
    return await BaseController.run(
        UserController.update_w8_form_confirmation, payload, request
    )