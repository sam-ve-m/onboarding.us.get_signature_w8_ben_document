# STANDARD IMPORTS
from pydantic import BaseModel


class W8FormConfirmation(BaseModel):
    w8_form_confirmation: bool
