# STANDARD IMPORTS
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    JWT_INVALID = 30
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100
    ERROR_LISTING_W8_BEN = 88
    ERROR_GETTING_W8_BEN = 40
    RESPONSE_ERROR_DRIVE_WEALTH = 50

    def __repr__(self):
        return self.value
