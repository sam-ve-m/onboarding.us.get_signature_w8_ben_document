def get_w8_form_confirmation_schema_template_with_data(
    w8_form_confirmation: str, unique_id: str
) -> dict:
    return {
        "unique_id": unique_id,
        "w8_form_confirmation": w8_form_confirmation,
    }
