from pydantic import BaseModel


class W8FormConfirmation(BaseModel):
    w8_confirmation: bool
