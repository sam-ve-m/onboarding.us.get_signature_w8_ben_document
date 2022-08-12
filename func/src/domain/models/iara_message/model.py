class IaraMessage:

    @classmethod
    def user_w8_signature_iara_schema(
            cls, unique_id: str
    ) -> dict:

        iara_template = {
            "unique_id": unique_id
        }

        return iara_template
