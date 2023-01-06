from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone

from func.src.domain.exceptions.exceptions import NotSentToPersephone
from func.src.domain.models.device_info.model import DeviceInfo
from func.src.domain.models.jwt.response import Jwt
from func.src.domain.models.w8_signature.base.model import W8FormConfirmation
from func.src.domain.persephone.template import W8ConfirmationToPersephone
from func.src.domain.persephone_queue.persephone_queue import PersephoneQueue


class SendToPersephone:
    @classmethod
    async def register_w8_confirmation_log(
        cls,
        jwt_data: Jwt,
        w8_confirmation_request: W8FormConfirmation,
        device_info: DeviceInfo,
    ):
        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_W8_CONFIRMATION_US.value,
            message=W8ConfirmationToPersephone.w8_form_confirmation_schema(
                w8_form_confirmation=w8_confirmation_request.w8_form_confirmation,
                unique_id=jwt_data.get_unique_id_from_jwt_payload(),
                device_info=device_info,
            ),
            schema_name="user_w8_form_confirmation_us_schema",
        )

        if sent_to_persephone is False:
            Gladsheim.error(
                message="SendToPersephone::register_user_exchange_member_log::Error on trying to register log"
            )
            raise NotSentToPersephone()
