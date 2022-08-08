# STANDARD IMPORTS
from decouple import config
from etria_logger import Gladsheim

# THIRD PART IMPORTS
from persephone_client import Persephone

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import NotSentToPersephone
from src.domain.models.jwt.response import Jwt
from src.domain.models.w8_signature.base.model import W8FormConfirmation
from src.domain.persephone.template import W8ConfirmationToPersephone
from src.domain.persephone_queue.persephone_queue import PersephoneQueue


class SendToPersephone:

    @classmethod
    async def register_w8_confirmation_log(
            cls,
            jwt_data: Jwt,
            w8_confirmation_request: W8FormConfirmation
    ):

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_W8_CONFIRMATION_US.value,
            message=W8ConfirmationToPersephone.w8_form_confirmation_schema(
                w8_form_confirmation=w8_confirmation_request.w8_form_confirmation,
                unique_id=jwt_data.get_unique_id_from_jwt_payload()
            ),
            schema_name="user_w8_form_confirmation_us_schema",
        )

        if sent_to_persephone is False:
            Gladsheim.error(
                message="SendToPersephone::register_user_exchange_member_log::Error on trying to register log")
            raise NotSentToPersephone
