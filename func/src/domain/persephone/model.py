class GetW8ConfirmationTemplate:

    @classmethod
    def get_w8_form_confirmation_schema_template_with_data(
        cls, w8_form_confirmation: str, unique_id: str
    ) -> dict:
        response = {
            "unique_id": unique_id,
            "w8_form_confirmation": w8_form_confirmation,
        }
        return response
