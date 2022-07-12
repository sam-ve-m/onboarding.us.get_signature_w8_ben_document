# STANDARD IMPORTS
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    JWT_INVALID = 30
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100
    RESPONSE_ERROR_DRIVE_WEALTH = 50
    WAS_NOT_SENT_TO_PERSEPHONE = 60

    def __repr__(self):
        return self.value
