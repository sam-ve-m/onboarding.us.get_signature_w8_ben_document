class W8ConfirmationToPersephone:
    @classmethod
    def w8_form_confirmation_schema(
        cls, w8_form_confirmation: str, unique_id: str
    ) -> dict:
        response = {
            "unique_id": unique_id,
            "w8_form_confirmation": w8_form_confirmation,
        }

        return response
