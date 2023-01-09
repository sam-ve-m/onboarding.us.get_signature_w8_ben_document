from func.src.domain.models.device_info.model import DeviceInfo


class W8ConfirmationToPersephone:
    @classmethod
    def w8_form_confirmation_schema(
        cls, w8_form_confirmation: str, unique_id: str, device_info: DeviceInfo
    ) -> dict:
        response = {
            "unique_id": unique_id,
            "w8_form_confirmation": w8_form_confirmation,
            "device_info": device_info.device_info,
            "device_id": device_info.device_id,
        }

        return response
